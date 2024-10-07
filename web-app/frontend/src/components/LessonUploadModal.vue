<template>
  <b-modal
    ref="lessonUploadModal"
    id="lesson-upload-modal"
    title="Passive Practice Session"
    @hide="initForm"
  >
    <div v-if="uploadStatus === 0">
      <b-form-group label-size="lg" label="Lesson Duration">
        <b-row id="lesson-duration">
          <b-col>
            <b-form-group description="Minutes">
              <b-form-input
                type="number"
                v-model="lessonDurationMinutes"
              ></b-form-input>
            </b-form-group>
          </b-col>
        </b-row>
      </b-form-group>
      <br />
    </div>
    <div v-else>
      <label for="upload-progress">
        <div v-if="uploadStatus === 1 || uploadStatus === 2">
          <b-icon icon="arrow-clockwise" animation="spin"></b-icon>
          Uploading...
        </div>
        <div v-else-if="uploadStatus === 3">
          <b-icon icon="check2-circle" variant="success" />
          Done Uploading!
        </div>
      </label>
      <b-progress
        v-if="uploadStatus === 1 || uploadStatus === 2"
        id="upload-progress"
        :value="currentStimuli"
        :max="activeScore.tactileStimuli.length - 1"
      />
    </div>

    <template #modal-footer>
      <b-button
        :disabled="uploadStatus > 0"
        variant="success"
        @click="initiateTactileFileTransfer"
      >
        <b-icon icon="play" />
        Start Passive Training Session
      </b-button>
    </template>
  </b-modal>
</template>

<script>
import { mapState } from 'vuex';
import bluetoothServices from '../services/bluetooth';

export default {
  data() {
    return {
      uploadStatus: 0,
      currentStimuli: 1,
      selectedLessons: [],
      formattedLessons: [],
      lessonRepeats: 10,
      lessonDurationMinutes: 120,
    };
  },
  computed: {
    ...mapState('bluetooth', ['glove', 'characteristic']),
    ...mapState('music', ['activeScore']),
    lessonDuration() {
      return this.lessonDurationMinutes * 60 * 1000;
    },
  },
  methods: {
    initForm() {
      this.uploadStatus = 0;
      this.currentStimuli = 1;
      this.selectedLessons = [];
      this.formattedLessons = this.activeScore.lessons.map((lesson, index) => ({
        text: `Lesson ${index + 1}`,
        value: lesson,
      }));
      this.lessonRepeats = 10;
      this.lessonDurationMinutes = 120;
    },
    formatTactileData() {
      const asterisks = '***';
      const { id, tactileStimuli, lessons } = this.activeScore;
      const filename = id.split('-')[0];
      const tactileMetadata = `${filename} ${tactileStimuli.length - 1} ${lessons.length} ${this.lessonDuration}`;
      const lessonData = this.activeScore.lessons.join(' ');
      let lessonOrder = '';
      let lessonTimes = '';
      this.activeScore.lessons.forEach((lesson) => {
        lessonOrder += `${this.activeScore.lessons.indexOf(lesson) + 1} `;
        lessonTimes += `${this.lessonRepeats} `;
      });
      return [asterisks, tactileMetadata, lessonData, lessonOrder, lessonTimes, asterisks];
    },
    async handleNotifications(event) {
      const { value } = event.target;
      const notification = parseInt(new TextDecoder().decode(value), 0);
      switch (notification) {
        case 0:
          console.log('file already exists.');
          bluetoothServices.stopNotifications(this.characteristic, this.handleNotifications);
          this.uploadStatus++;
          break;
        case 1:
          console.log('file does not exist, start transmission.');
          await this.until((_) => this.uploadStatus === 2);
          this.sendTactileStimuliData();
          break;
        case 2:
          console.log('successful transmission.');
          bluetoothServices.stopNotifications(this.characteristic, this.handleNotifications);
          this.uploadStatus++;
          break;
        case 3:
          console.log('failed transmission.');
          bluetoothServices.stopNotifications(this.characteristic, this.handleNotifications);
          this.uploadStatus = 0;
          break;
        default:
          break;
      }
    },
    async sendTactileStimuliData() {
      const hyphens = '---';
      await bluetoothServices.writeDataToCharacteristic(hyphens, this.characteristic);
      const { tactileStimuli } = this.activeScore;
      while (this.currentStimuli < tactileStimuli.length) {
        const tactileStimulus = `${this.currentStimuli} ${tactileStimuli[this.currentStimuli]}`;
        await bluetoothServices.writeDataToCharacteristic(tactileStimulus, this.characteristic);
        this.currentStimuli += 1;
      }
      await bluetoothServices.writeDataToCharacteristic(hyphens, this.characteristic);
    },
    async initiateTactileFileTransfer() {
      this.uploadStatus++;
      await bluetoothServices.startNotifications(this.characteristic, this.handleNotifications);
      const metadata = this.formatTactileData();
      for (let i = 0; i < metadata.length; i++) {
        await bluetoothServices.writeDataToCharacteristic(metadata[i], this.characteristic);
      }
      this.uploadStatus++;
    },
    until(condition) {
      const poll = (resolve) => {
        if (condition()) resolve();
        else setTimeout((_) => poll(resolve), 200);
      };

      return new Promise(poll);
    },
  },
  mounted() {
    this.initForm();
  },
};
</script>
