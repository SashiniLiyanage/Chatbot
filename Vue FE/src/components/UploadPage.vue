
<template>
  <div class="bg">
  <button @click="goToChatBox">Chat Bot</button>
  <div class="chatbox-container">
  <div class="container">
    <h1>Upload Content</h1>
    <div class="upload-actions">
      <input type="file" ref="fileInput" @change="handleFileChange" style="display: none" multiple accept=".pdf"/>
      <button class="selectButton" @click="showFileInput">Select Files</button>
      <div v-if="selectedFiles.length>0">{{ selectedFiles.length }} files</div>
      <button :disabled="uploading || processing" class="uploadButton" @click="uploadFiles">Upload</button>
      <div style="flex: 1"></div>
      <div>{{ count }} Files</div>
      <button :disabled="uploading || processing" :class="processing? 'processButton processing' :'processButton'" @click="processFiles">
        <span v-if="processing">Processing...</span>
        <span v-else>Process</span>
      </button>
    </div>
  <div class="messageBox chat_area"  ref="scrollableDiv">
  <div>
    <table class="pdf-table">
      <tbody>
        <tr v-for="(fileName, index) in fileNames" :key="index">
          <td>{{ fileName }}</td>
          <td class="delete-icon">
            <button class="deleteButton" @click="deleteFile(fileName)">❌</button>
            <!-- Add other actions as needed -->
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  </div>
  </div>
  </div>
  </div>
  </template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFiles: [],
      fileNames: [],
      uploading: false,
      processing: false,
      count : 0
    };
  },
  mounted() {
    this.fetchFileList();
  },
  methods: {
    goToChatBox() {
      this.$router.push("/");
    },
    showFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileChange() {
      this.selectedFiles = this.$refs.fileInput.files;
    },
    uploadFiles() {
      if (this.selectedFiles.length == 0) return;
      const formData = new FormData();
      for (let i = 0; i < this.selectedFiles.length; i++) {
        formData.append('pdfs', this.selectedFiles[i]);
        console.log(i)
      }

      this.uploading = true
      axios.post(process.env.VUE_APP_BE_URL+'/upload', formData)
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        }).finally(()=>{
          this.uploading = false;
          this.selectedFiles = [];
          this.fetchFileList()
        });
    },
    processFiles() {
      this.processing = true
      axios.post(process.env.VUE_APP_BE_URL+'/process')
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        }).finally(()=>{
          this.processing = false;
        });
    },
    fetchFileList() {
      fetch(process.env.VUE_APP_BE_URL+'/list_files')
        .then((response) => response.json())
        .then((data) => {
          this.fileNames = data;
          this.count = data.length
        })
        .catch((error) => {
          console.error('Error fetching file list:', error);
        });
    },
    deleteFile(fileName) {
      axios.post(process.env.VUE_APP_BE_URL+'/delete_files',{
        fileName: fileName
      })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error(error);
      }).finally(()=>{
        this.fetchFileList();
      });
    },
  },
};
</script>