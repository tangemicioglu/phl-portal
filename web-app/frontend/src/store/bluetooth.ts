import bluetoothServices from '@/services/bluetooth';
import { TableLitePlugin } from 'bootstrap-vue';
import 'web-bluetooth';

interface BluetoothState {
  glove: BluetoothDevice | undefined;
  gatt: BluetoothRemoteGATTServer | undefined;
  characteristic: BluetoothRemoteGATTCharacteristic | undefined;
  isGloveConnected: boolean;
}

const initialState: BluetoothState = {
  glove: undefined,
  gatt: undefined,
  characteristic: undefined,
  isGloveConnected: false,
};

const bluetooth = {
  namespaced: true,
  state: {
    glove: undefined,
    gatt: undefined,
    characteristic: undefined,
    isGloveConnected: false,
  },
  mutations: {
    updateGlove(state: BluetoothState, glove: BluetoothDevice) {
      state.glove = glove;
      if (glove.gatt) {
        state.gatt = glove.gatt;
        state.isGloveConnected = glove.gatt.connected;
      } else {
        state.isGloveConnected = false;
      }
    },
    updateCharacteristic(state: BluetoothState, characteristic: BluetoothRemoteGATTCharacteristic) {
      state.characteristic = characteristic;
    },
  },
  actions: {
    async scanForGlove({ dispatch }): Promise<boolean> {
      try {
        const device = await bluetoothServices.scanForDevice();
        const connection = await dispatch('connectToGlove', device);
        return connection;
      } catch (error) {
        console.log(error);
        return false;
      }
    },
    async connectToGlove({ commit }, glove: BluetoothDevice): Promise<boolean> {
      try {
        const characteristic = await bluetoothServices.connectToDevice(glove, (event) => commit('updateGlove', event.target));
        commit('updateCharacteristic', characteristic);
        commit('updateGlove', glove);
        return true;
      } catch (error) {
        console.log(error);
        return false;
      }
    },
    disconnectFromGlove({ state }) {
      bluetoothServices.disconnectFromDevice(state.glove);
    },
  },
};

export default bluetooth;
