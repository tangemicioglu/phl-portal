import 'web-bluetooth';

const SERVICE_UUID = process.env.VUE_APP_SERVICE_UUID;
const CHARACTERISTIC_UUID_RX = process.env.VUE_APP_CHARACTERISTIC_UUID_RX;

async function getDevices() {
  return window.navigator.bluetooth.getDevices();
}
async function scanForDevice(): Promise<BluetoothDevice> {
  return window.navigator.bluetooth.requestDevice({
    filters: [{ services: [SERVICE_UUID] }],
  });
}

async function connectToDevice(device: BluetoothDevice, disconnectionHandler?: (e: Event) => void):
  Promise<BluetoothRemoteGATTCharacteristic> {
  if (device.gatt) {
    const server = await device.gatt.connect();
    const service = await server.getPrimaryService(SERVICE_UUID);
    const characteristic = await service.getCharacteristic(CHARACTERISTIC_UUID_RX);
    if (disconnectionHandler) {
      device.addEventListener('gattserverdisconnected', disconnectionHandler);
    }
    return characteristic;
  }
  return Promise.reject();
}

async function writeDataToCharacteristic(data: string,
  characteristic: BluetoothRemoteGATTCharacteristic):
  Promise<boolean> {
  if (!data || !characteristic) {
    return false;
  }
  // console.log(`Sending ${data} to ${characteristic.uuid}`);
  const encodedData = new TextEncoder().encode(data);
  await characteristic.writeValue(encodedData);
  return true;
}

function disconnectFromDevice(device: BluetoothDevice) {
  if (device && device.gatt && device.gatt.connected) {
    device.gatt.disconnect();
  }
}

async function startNotifications(characteristic: BluetoothRemoteGATTCharacteristic,
  notificationHandler: (e: Event) => void) {
  if (characteristic) {
    await characteristic.startNotifications();
    characteristic.addEventListener('characteristicvaluechanged', notificationHandler);
  }
  return false;
}

async function stopNotifications(characteristic: BluetoothRemoteGATTCharacteristic,
  notificationHandler: (e: Event) => void) {
  if (characteristic) {
    await characteristic.stopNotifications();
    characteristic.removeEventListener('characteristicvaluechanged', notificationHandler);
  }
  return false;
}

export default {
  getDevices,
  scanForDevice,
  connectToDevice,
  disconnectFromDevice,
  writeDataToCharacteristic,
  startNotifications,
  stopNotifications,
};
