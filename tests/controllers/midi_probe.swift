// Controlled virtual MIDI source. Input: three hex bytes per stdin line; quit ends.
// No hardware endpoints are opened and no installed files are changed.
import Foundation
import CoreMIDI

var client: MIDIClientRef = 0
var source: MIDIEndpointRef = 0
var destination: MIDIEndpointRef = 0
let name = "Codex Definition Probe"
func check(_ status: OSStatus) {
    if status != noErr { fatalError("CoreMIDI status \(status)") }
}
check(MIDIClientCreate(name as CFString, nil, nil, &client))
check(MIDISourceCreate(client, name as CFString, &source))
check(MIDIDestinationCreateWithBlock(client, name as CFString, &destination) { _, _ in })
print("READY \(name)")
fflush(stdout)
while let line = readLine() {
    if line == "quit" { break }
    let bytes = line.split(separator: " ").compactMap { UInt8($0, radix: 16) }
    guard bytes.count == 3 else { print("ERROR expected three hex bytes"); fflush(stdout); continue }
    var packetList = MIDIPacketList()
    withUnsafeMutablePointer(to: &packetList) { list in
        let packet = MIDIPacketListInit(list)
        bytes.withUnsafeBufferPointer { buffer in
            _ = MIDIPacketListAdd(list, MemoryLayout<MIDIPacketList>.size, packet, 0,
                                  bytes.count, buffer.baseAddress!)
        }
        check(MIDIReceived(source, list))
    }
    print("SENT \(line)")
    fflush(stdout)
}
MIDIEndpointDispose(destination)
MIDIEndpointDispose(source)
MIDIClientDispose(client)
