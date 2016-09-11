require('file?name=[name].[ext]!../html/index.html');

import Vue from 'vue';
import VueResource from 'vue-resource';

Vue.use(VueResource);

let classifyApi = '/classify'
if (process.env.NODE_ENV !== 'production') {
  classifyApi = 'http://localhost:5000/classify'
}

new Vue({
  el: '#form',
  data: {
    content: '',
    result: {},
    isFetching: false,
    isFailed: null,
    error: null,
  },
  methods: {
    requestClassify: function() {
      this.isFetching = true;
      this.$http.post(classifyApi, {content: this.content}).then((response) => {
        // success callback
        if (response.body.ok) {
          this.result = response.body.result;
          this.isFailed = false;
        } else {
          this.result = {};
          this.isFailed = true;
          this.error = response.body.error;
        }

        this.isFetching = false;
      }, (response) => {
        // error callback
        this.result = {};
        this.isFetching = false;
        this.isFailed = true;
      });
    }
  }
});
