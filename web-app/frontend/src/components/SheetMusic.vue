<template>

  <b-card header="Sheet Music" header-tag="nav">
  <template #header>
    <div class="vld-parent">
      <loading :active.sync="notLoaded"
               :can-cancel="true"
               :is-full-page="true"></loading>
    </div>
    <b-nav card-header>
      <b-navbar-brand> Sheet Music </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right variant="dark">
          <template #button-content>
            <b-icon icon="gear" />
          </template>
          <b-dropdown-form>
            <label for="tempo-spinner">Tempo: </label>
            <b-form-spinbutton
              id="tempo-spinner"
              :formatter-fn="tempoFormatter"
              step="2"
              v-model="tempo"
              @change="updateTempo"
              min="40"
              max="160"
              class="mx-1"
              inline
            />
          </b-dropdown-form>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-nav>
  </template>

  <b-skeleton-img animation="fade" v-if="this.osmd == null" />
  <div id="floatingButtonPlay" @click = "playScore">
  <fab
    :main-icon="mainIcon"
    ></fab>
  </div>
  <!-- eslint-disable-next-line max-len -->
  <div id="floatingButtonStop" @click.stop = "handleFloatingButtonStopPressed">
    <fab
    :main-icon="mainIconStop"
    :position = "position"
    ></fab>
  </div>
  <div>
    <b-alert
    :show="recordingCountdown"
    dismissible
    variant="warning"
    @dismissed="recordingCountdown=0"
    @dismiss-count-down="recordingCountdown">
      <p>Score starting in {{ recordingCountdown }} seconds...</p>
    </b-alert>

  </div>
  <div id="osmdContainer" />
  <b-button-toolbar>
    <b-button class="mx-1" @click="playScore">
      <b-icon icon="play" aria-hidden="true" />
      Play
    </b-button>
    <b-button class="mx-1" @click="playScore(true)">
        <b-icon icon="music-note-list" aria-hidden="true" />
        Practice
    </b-button>
    <div id="record-track">
      <b-tooltip
        v-if="!this.isMIDIDeviceConnected"
        target="record-track"
        triggers="hover"
      >
        Connect a compatible MIDI device to enable recording.
      </b-tooltip>
      <b-button class="mx-1" id="recordButton"
      :disabled="!this.isMIDIDeviceConnected"
      @click="handleRecordClick()" >
        <b-icon icon="record2" aria-hidden="true" />
        Record
      </b-button>
    </div>
    <div id="record-tooltip">
      <b-button
        class="mx-1"
        v-b-modal.recording-upload-modal
      >
        Upload Performance
      </b-button>
    </div>
    <RecordingUploadModal />
    <div id="passive-practice-tooltip">
      <b-tooltip
        v-if="!this.isGloveConnected"
        target="passive-practice-tooltip"
        triggers="hover"
      >
        Connect your PHL Gloves to enable passive practice.
      </b-tooltip>
      <b-button
        class="mx-1"
        :disabled="!this.isGloveConnected"
        v-b-modal.lesson-upload-modal
      >
        Begin Passive Practice Session
      </b-button>
    </div>
  </b-button-toolbar>
  <LessonUploadModal />
</b-card>
</template>

<script>
/* eslint-disable */
import { mapState, mapActions } from 'vuex';
import { OpenSheetMusicDisplay } from 'opensheetmusicdisplay';
// Import component
import Loading from 'vue-loading-overlay';
// Import stylesheet
import 'vue-loading-overlay/dist/vue-loading.css';
import AudioPlayer from 'osmd-audio-player';
import LessonUploadModal from './LessonUploadModal.vue';
import RecordingUploadModal from './RecordingUploadModal.vue';
import midiServices from '../services/midi';
import FAB from 'vue-fab';

export default {
data() {
  return {
    el: '#record-track',
    osmd: null,
    audioPlayer: null,
    currentLessonIndex: 0,
    tempo: 100,
    isRecording: false,
    eventArray: [],
    DateTimeStamps: [],
    recordingTimeoutIDs: [],
    mainIcon: 'play_circle',
    mainIconStop: 'stop_circle',
    position: 'bottom-left',
    isPlaying: false,
    accidentals: {},
    numPlays: 0,
    last_event: null,
    isPractice: false,
    recordingCountdown: 0,
    notLoaded: true
  };
},
computed: {
  currentLesson() {
    return this.activeScore.lessons[this.currentLessonIndex];
  },
  ...mapState('music', ['activeScore']),
  ...mapState('midi', ['isMIDIDeviceConnected', 'midiOutput']),
  ...mapState('bluetooth', ['isGloveConnected']),
},
watch: {
  currentLesson(lesson) {
    this.initAudioPlayer(lesson);
  },
},
components: {
  LessonUploadModal,
  RecordingUploadModal,
  Loading,
  fab:FAB,
},
methods: {
  ...mapActions('music', ['fetchXML']),
  muteScore() {
    this.osmd.Sheet.instruments.forEach(
        (instrument) => {
          instrument.voices.forEach(
            (voice)=> {
              voice.voiceEntries.forEach(
                (entry)=> {
                  entry.articulations = [];
                }
              )
            }
          )
        }
      )
      console.log("Load Score")
      this.audioPlayer.loadScore(this.osmd);
      this.audioPlayer.scoreInstruments.forEach(
        (instrument) => {
          instrument.voices[0].volume = 0;
          instrument.voices[1].volume = 0;
        }
      )
  },
  unmuteScore() {
      this.audioPlayer.scoreInstruments.forEach(
        (instrument) => {
          instrument.voices[0].volume = 1;
          instrument.voices[1].volume = 1;
        }
      )
  },
  handleRecordClick() {
    // console.log(this.recordButton);
    this.isRecording = !this.isRecording;
    if (this.isRecording === true) {
      this.eventArray = [];
      this.DateTimeStamps = [];
      this.$el.querySelector('#recordButton').textContent = 'Stop Recording';
      this.$el.querySelector('#recordButton').classList.remove('btn-primary');
      this.$el.querySelector('#recordButton').classList.add('btn-danger');
      this.muteScore()
      var that = this
      that.$el.querySelector('#recordButton').textContent = '3';
      that.recordingCountdown = 3;
      this.recordingTimeoutIDs.push(setTimeout(function() {
        that.$el.querySelector('#recordButton').textContent = '2';
        that.recordingCountdown = 2;
      }, 1000));
      this.recordingTimeoutIDs.push(setTimeout(function() {
        that.$el.querySelector('#recordButton').textContent = '1';
        that.recordingCountdown = 1;
      }, 2000));
      this.recordingTimeoutIDs.push(setTimeout(function() {
        that.playScore();
        that.$el.querySelector('#recordButton').textContent = 'Stop Recording';
      }, 3000));
    } else {
      this.last_event = null;
      this.$el.querySelector('#recordButton').textContent = 'Record';
      this.$el.querySelector('#recordButton').classList.remove('btn-danger');
      this.$el.querySelector('#recordButton').classList.add('btn-primary');
      // console.log('%%%%', this.eventArray);
      this.unmuteScore();
      this.stopScore();
      this.recordingTimeoutIDs.forEach((timeoutId) => {
        clearTimeout(timeoutId);
      })
      this.recordingTimeoutIDs.length = 0;

      const MIDI_MESSAGE_TYPE = {
        DRUMPAD_HOLD: 153,
        DRUMPAD_RELEASE: 137,
        KNOB_ROTATE: 176,
        KEY_PRESS: 144,
        KEY_RELEASE: 128,
      };
      let current_notes = [];
      let notes = [];
      for (let i = 0; i < this.eventArray.length; i++) {
        var event = this.eventArray[i];
        var timestamp = this.DateTimeStamps[i];
        const typeId = event.data[0];
        const noteNumber = event.data[1];
        const Velocity = event.data[2];
        switch (typeId) {
          case MIDI_MESSAGE_TYPE.KEY_PRESS:
            current_notes.push(noteNumber)
            notes.push({
                key: noteNumber,
                length: 212,
                start_time: timestamp,
                velocity: Velocity,
                end_time: null
              })
            break;
          case MIDI_MESSAGE_TYPE.KEY_RELEASE:
            var index = current_notes.indexOf(noteNumber);
            if (index !== -1) {
                current_notes.splice(index, 1);
            }
            var notes_index = notes.map(object => object.key).indexOf(noteNumber);
            notes[notes_index].end_time = timestamp;
            notes[notes_index].length = event.end_time - event.start_time;
            break;
          default:
            break;
        }
      }
      // eventTimes.push(last_keyrelease_time)
      this.eventArray = [];
      // *****************
      var BPM, PPQN, blob, event, events, first_track_events, iso_date_string, l, last_time, len3, len4, m, midi_file, note, output_array_buffer, pulses_per_ms, recording_name, total_track_time_ms, total_track_time_seconds;
      console.log("new MIDIFile")

      midi_file = new MIDIFile();
      // console.log(notes);
      if (notes.length === 0) {
        alert("No notes have been recorded!");
        try {
          localStorage[`to_delete:${active_recording_session_id}`] = `no_notes ${new Date().toISOString()}`;
        } catch (error1) {}
        return;
      }
      events = [];
      for (l = 0, len3 = notes.length; l < len3; l++) {
        note = notes[l];
        events.push({
          delta: null,
          _time: note.start_time,
          type: MIDIEvents.EVENT_MIDI,
          subtype: MIDIEvents.EVENT_MIDI_NOTE_ON,
          channel: 0,
          param1: note.key,
          param2: note.velocity
        });
        if (note.end_time != null) {
          events.push({
            delta: null,
            _time: note.end_time,
            type: MIDIEvents.EVENT_MIDI,
            subtype: MIDIEvents.EVENT_MIDI_NOTE_OFF,
            channel: 0,
            param1: note.key,
            param2: 5 // TODO?
          });
        }
      }
      // TODO: EVENT_MIDI_CHANNEL_AFTERTOUCH
      events = events.filter(function(event) {
        return isFinite(event._time);
      });
      events.sort(function(a, b) {
        return a._time - b._time;
      });
      total_track_time_ms = events[events.length - 1]._time - events[0]._time;
      total_track_time_ms += 1000; // extra time for notes to ring out
      BPM = 120; // beats per minute
      PPQN = 192; // pulses per quarter note
      pulses_per_ms = PPQN * BPM / 60000;
      total_track_time_seconds = total_track_time_ms / 1000;
      last_time = null;
      for (m = 0, len4 = events.length; m < len4; m++) {
        event = events[m];
        if (event.delta == null) {
          if (last_time != null) {
            event.delta = (event._time - last_time) * pulses_per_ms;
          } else {
            event.delta = 0;
          }
          if (isFinite(event._time)) {
            last_time = event._time;
          }
        }
        delete event._time;
      }
      events.push({
        delta: 0,
        type: MIDIEvents.EVENT_META,
        subtype: MIDIEvents.EVENT_META_END_OF_TRACK,
        length: 0
      });
      first_track_events = [
        {
          delta: 0,
          type: MIDIEvents.EVENT_META,
          subtype: MIDIEvents.EVENT_META_TIME_SIGNATURE,
          length: 4,
          data: [4,
        2,
        24,
        8],
          param1: 4,
          param2: 2,
          param3: 24,
          param4: 8
        },
        {
          delta: 0,
          type: MIDIEvents.EVENT_META,
          subtype: MIDIEvents.EVENT_META_SET_TEMPO,
          length: 3,
          tempo: 60000000 / BPM
        },
        {
          delta: ~~(total_track_time_ms * pulses_per_ms),
          type: MIDIEvents.EVENT_META,
          subtype: MIDIEvents.EVENT_META_END_OF_TRACK,
          length: 0
        }
      ];
      midi_file.setTrackEvents(0, first_track_events);
      midi_file.addTrack(1);
      midi_file.setTrackEvents(1, events);
      //	console.log({first_track_events, events})
      output_array_buffer = midi_file.getContent();
      console.log("new Blob")

      blob = new Blob([output_array_buffer], {
        type: "audio/midi"
      });
      console.log("new Date")

      let x = new Date();
      let y = new Date(x.getTime()- new Date().getTimezoneOffset()*60*1000 ).toISOString();
      const file_name = this.activeScore.filename.split('.')[0] + "_" + y.split('.')[0] + "_" + y.split('.')[1] + ".midi";
      // Bartok_For_Children_2022-08-25T01_38_18_624Z.midi
      saveAs(blob, file_name);
      this.eventArray = [];
      notes = [];
      events = [];
    }
  },
  async handleFloatingButtonStopPressed() {
    console.log(this.isRecording)
    if(this.isRecording) {
      this.handleRecordClick();
    } else {
      this.stopScore();
    }
  },
  async playScore(practiceMode) {
    this.isPractice = practiceMode != null && practiceMode === true ? true : false;
    console.log("playScore")
    if (this.isPlaying === true) {
      this.isPlaying = false;
      this.mainIcon = 'play_circle';
      console.log("pause")
      this.audioPlayer.pause();
    } else {
      this.isPlaying = true;
      this.mainIcon = 'pause_circle';
      console.log("play")
      this.audioPlayer.play();
      this.numPlays += 1;
    }
  },
  async stopScore() {
    console.log("stopScore")

    this.accidentals = {};
    console.log("stop")
    await this.audioPlayer.stop();
    this.osmd.cursor.reset();
    this.osmd.cursor.show();
    this.mainIcon = 'play_circle';
    this.isPlaying = false;
    //console.log("Load Score")
    //await this.audioPlayer.loadScore(this.osmd);
  },
  onMIDIMessage(event) {
    if(this.isRecording === true){
        if((this.last_event ==null) || !(event.data[0] === this.last_event.data[0] && event.data[1] === this.last_event.data[1] && event.data[2] === this.last_event.data[2] && event.timeStamp === this.last_event.timeStamp)){
          this.DateTimeStamps.push(Date.now());
          this.eventArray.push(event);
      }
      this.last_event = event;
    }
  },
  updateTempo(bpm) {
    this.tempo = bpm;
    this.audioPlayer.setBpm(bpm);
  },
  initAudioPlayer(lesson) {
    console.log("initAudioPlayer")
    this.audioPlayer.stop();
    this.osmd.cursor.reset();
    this.audioPlayer.jumpToStep(lesson - 2);
  },
  tempoFormatter(value) {
    return `${value} bpm`;
  },
  onIteration(notes) {
    // const nextLesson = this.activeScore.lessons[this.activeScore.lessons.length];
    // if (this.audioPlayer.currentIterationStep === (this.activeScore.lessons).length - 1 ) {
    //   this.initAudioPlayer(0);
    //   return;
    // }
    // console.log(">>", this.audioPlayer.state);
    // this.osmd.cursor.show();
    // console.log(`onIteration() => isPlaying: ${this.isPlaying}`);
    // Don't send note to MIDI for practice mode
    if (this.isPractice) return;
    if (this.isRecording) return;
    // console.log("Note sent to MIDI Device");
    notes.forEach((note) => {
      if (this.isMIDIDeviceConnected && !note.isRestFlag && note.pitch && note.length) {
        const beats = note.length.realValue * 4;
        const secondsPerBeat = 60 / this.tempo;
        const duration = beats * secondsPerBeat * 1000;
        let key = note.sourceMeasure.MeasureNumberXML.toString + "_" + note.pitch.fundamentalNote.toString()+"_"+note.pitch.octave.toString();
        let inDict = this.accidentals.hasOwnProperty(key);
        let initPitch = note.pitch.fundamentalNote;
        if(note.pitch.accidentalXml === 'flat' || (inDict && this.accidentals[key] === 'flat') ){
          initPitch = note.pitch.fundamentalNote - 1;
          if(!inDict){
            this.accidentals[key] = 'flat';
          }
        }
        if(note.pitch.accidentalXml === 'sharp' || (inDict && this.accidentals[key] === 'sharp') ){
          initPitch = note.pitch.fundamentalNote + 1;
          if(!inDict){
            this.accidentals[key] = 'sharp';
          }
        }
        const pitch = initPitch + (note.pitch.octave - 1) * 12;
        midiServices.playNote(this.midiOutput, pitch, duration)
        // console.log(note,pitch);
        // note.sourceMeasure.MeasureNumberXML, note.pitch.octave, // or measureNumber
        // connection: "open"
        // id: "output-1"
        // manufacturer: "Casio Computer Co., Ltd"
        // name: "CASIO USB-MIDI"
        // onstatechange: null
        // state: "connected"
        // type: "output"
        // version: "1.0"
      }
    });
    const { cursor } = this.osmd;
  },
},
async created() {
  await this.fetchXML();
  const osmd = new OpenSheetMusicDisplay('osmdContainer', {
    followCursor: false,
    autoResize: false,
  });
  await osmd.load(this.activeScore.xml);
  await this.$nextTick();
  await osmd.render();
  this.osmd = osmd;
  this.osmd.cursor.show();
  const audioPlayer = new AudioPlayer();

  audioPlayer.on('iteration', (notes) => this.onIteration(notes));

  this.audioPlayer = audioPlayer;
  this.tempo = this.audioPlayer.playbackSettings.bpm;
  console.log("Load Score")
  await this.audioPlayer.loadScore(osmd);
  await this.audioPlayer.loadScore(osmd);
  this.notLoaded = false
},
beforeUpdate() {
  navigator.requestMIDIAccess().then((midiAccess) => {
    midiAccess.inputs.forEach((input) => {
      input.onmidimessage = this.onMIDIMessage;
    });
  });
},
};
</script>
