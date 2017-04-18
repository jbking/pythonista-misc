import cb
import sound
import time
import struct


class Mesh:
    name = None
    service = '72C90001-57A9-4D40-B746-534E22EC9F9E'

    class Characteristic:
        notify = '72C90003-57A9-4D40-B746-534E22EC9F9E'
        write_without_response = '72C90002-57A9-4D40-B746-534E22EC9F9E'
        indicate = '72C90005-57A9-4D40-B746-534E22EC9F9E'
        write = '72C90004-57A9-4D40-B746-534E22EC9F9E'


class MeshButton(Mesh):
    name = 'MESH-100BU1004629'


# future plan
# class MeshLED(Mesh):
#     name = 'MESH-100LE1004443'


class MeshManager:
    def __init__(self):
        self.peripheral = None
        self._peripheral_state = None

    @property
    def peripheral_state(self):
        return self._peripheral_state
    
    @peripheral_state.setter
    def peripheral_state(self, value):
        print('peripheral_state %s => %s' % (self._peripheral_state, value))
        self._peripheral_state = value
        attr = getattr(self, value, None)
        if callable(attr):
            attr()
        
    def did_discover_peripheral(self, p):
        if not p.name:
            return
        if p.name == MeshButton.name:
            if self.peripheral:
                print('Already connected to MESH Button')
            else:
                self.peripheral = p
                print('Connecting to MESH Button...')
                cb.connect_peripheral(p)
                cb.stop_scan()

    def did_connect_peripheral(self, p):
        print('Connected:', p.name)
        print('Discovering services...')
        p.discover_services()

    def did_fail_to_connect_peripheral(self, p, error):
        print('Failed to connect: %s %s' % (p.namme, error))

    def did_disconnect_peripheral(self, p, error):
        print('Disconnected, error: %s %s' % (p.name, error))
        self.peripheral = None

    def did_discover_services(self, p, error):
        for s in p.services:
            print('service uuid:', s.uuid)
            if s.uuid == MeshButton.service:
                print('Discovered MESH Button service, discovering characteristitcs...')
                p.discover_characteristics(s)

    def did_discover_characteristics(self, s, error):
        print('Did discover characteristics...')
        for c in s.characteristics:
            print('characteristic uuid:', c.uuid)
            if c.uuid == MeshButton.Characteristic.indicate:
                self.char_indicate = c
            elif c.uuid == MeshButton.Characteristic.write:
                self.char_write = c
            elif c.uuid == MeshButton.Characteristic.notify:
                self.char_notify = c
        if self.char_indicate and self.char_write and self.char_notify:
            print('Setup characteristics')
            self.peripheral_state = 'set_notify'
            self.peripheral.set_notify_value(self.char_indicate, True)
        else:
            print('Something in bad condition, failed')
            self.die()

    def did_write_value(self, c, error):
        if error:
            print('error at did_write_value with: %s %s' % (c.uuid, error))
        if c.uuid == MeshButton.Characteristic.write and self.peripheral_state == 'write_state':
            self.peripheral_state = 'ready'
            self.peripheral.set_notify_value(self.char_notify, True)
                    
    def did_update_value(self, c, error):
        if error:
            print('error at did_update_value: %s %s', (c.uuid, error))
            return
        if self.peripheral_state == 'set_notify':
            self.peripheral_state = 'write_state'
            # communicate in big-endian
            send_data = struct.pack('>L', 0x00020103)
            self.peripheral.write_characteristic_value(self.char_write, send_data, True)
        elif self.peripheral_state == 'ready':
            if c.uuid == MeshButton.Characteristic.notify:
                if len(c.value) != 4:
                    # unknown
                    print('Unknown:', c.value)
                    return
                result = struct.unpack('>L', c.value)[0]
                if result == 0x01000102:
                    self.press()
                elif result == 0x01000203:
                    self.hold()
                elif result == 0x01000304:
                    self.double_press()
                else:
                    print('Wrong format or unknown?:', hex(result))

    def die(self):
        if self.peripheral:
            cb.cancel_peripheral_connection(self.peripheral)
            print('called cb.cancel_peripheral_connection: ', self.peripheral.name)

    def press(self):
        print('MESH Button Pressed')
    
    def hold(self):
        print('MESH Button Held')
    
    def double_press(self):
        print('MESH Button Double Pressed')


if __name__ == '__main__':
    delegatee = MeshManager()
    cb.set_verbose(True)
    cb.set_central_delegate(delegatee)
    print('Scanning for peripherals...')
    cb.scan_for_peripherals()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        delegatee.die()
        cb.reset()
        print('called cb.reset()')
