// Long-lived virtual MIDI source for multi-step tests, driven by a command file.
//
// midi_probe.swift reads stdin, which is fine inside one process but not across
// separate steps: a background process here does not reliably outlive the shell
// that started it, and a FIFO whose reader has died blocks the writer forever.
// This variant owns the endpoint for a bounded lifetime and takes commands by
// appending lines to a file, so the device stays visible in VirtualDJ's
// Controllers list while a person selects a mapping for it.
//
// usage: midi-daemon <command-file> <seconds>
// Append "90 24 7f" (three hex bytes) to send; append "quit" to stop early.
// Progress is written to <command-file>.log. No hardware ports are opened and
// no installed files are changed.
import Foundation
import CoreMIDI

let arguments = CommandLine.arguments
guard arguments.count == 3, let lifetime = Double(arguments[2]) else {
    FileHandle.standardError.write("usage: midi-daemon <command-file> <seconds>\n".data(using: .utf8)!)
    exit(2)
}
let commandPath = arguments[1]
let logPath = commandPath + ".log"
let name = "Codex Definition Probe"

var client: MIDIClientRef = 0
var source: MIDIEndpointRef = 0
var destination: MIDIEndpointRef = 0

func log(_ message: String) {
    let line = message + "\n"
    if let handle = FileHandle(forWritingAtPath: logPath) {
        handle.seekToEndOfFile()
        handle.write(line.data(using: .utf8)!)
        handle.closeFile()
    } else {
        try? line.write(toFile: logPath, atomically: true, encoding: .utf8)
    }
}

func check(_ status: OSStatus, _ what: String) {
    if status != noErr { log("ERROR \(what) \(status)"); exit(1) }
}

FileManager.default.createFile(atPath: logPath, contents: nil)
FileManager.default.createFile(atPath: commandPath, contents: nil)
check(MIDIClientCreate(name as CFString, nil, nil, &client), "client")
check(MIDISourceCreate(client, name as CFString, &source), "source")
check(MIDIDestinationCreateWithBlock(client, name as CFString, &destination) { _, _ in }, "destination")
log("READY \(name) for \(Int(lifetime))s")

func send(_ bytes: [UInt8]) {
    var packetList = MIDIPacketList()
    withUnsafeMutablePointer(to: &packetList) { list in
        let packet = MIDIPacketListInit(list)
        bytes.withUnsafeBufferPointer { buffer in
            _ = MIDIPacketListAdd(list, MemoryLayout<MIDIPacketList>.size, packet, 0,
                                  bytes.count, buffer.baseAddress!)
        }
        check(MIDIReceived(source, list), "send")
    }
}

// Only lines added since the last poll are executed, so re-reading the whole
// file never replays an earlier note.
var consumed = 0
let deadline = Date().addingTimeInterval(lifetime)
while Date() < deadline {
    let text = (try? String(contentsOfFile: commandPath, encoding: .utf8)) ?? ""
    let lines = text.split(separator: "\n", omittingEmptySubsequences: false).map(String.init)
    let complete = text.hasSuffix("\n") ? lines.count - 1 : lines.count - 1
    if complete > consumed {
        for line in lines[consumed..<complete] {
            let trimmed = line.trimmingCharacters(in: .whitespaces)
            if trimmed.isEmpty { continue }
            if trimmed == "quit" { log("QUIT"); consumed = complete; break }
            let bytes = trimmed.split(separator: " ").compactMap { UInt8($0, radix: 16) }
            guard bytes.count == 3 else { log("ERROR expected three hex bytes: \(trimmed)"); continue }
            send(bytes)
            log("SENT \(trimmed)")
        }
        if lines[consumed..<complete].contains(where: { $0.trimmingCharacters(in: .whitespaces) == "quit" }) {
            break
        }
        consumed = complete
    }
    usleep(150_000)
}
log("DISPOSED")
MIDIEndpointDispose(destination)
MIDIEndpointDispose(source)
MIDIClientDispose(client)
