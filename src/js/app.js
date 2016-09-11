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
  },
  methods: {
    requestClassify: function() {
      this.isFetching = true;
      this.$http.post(classifyApi, {content: this.content}).then((response) => {
        // success callback
        this.result = response.body.result;
        this.isFetching = false;
        this.isFailed = false;
      }, (response) => {
        // error callback
        this.result = null;
        this.isFetching = false;
        this.isFailed = true;
      });
    }
  }
});
