import './styles.css';
import ChatBox from "./components/ChatBox.vue";
import UploadPage from "./components/UploadPage.vue";
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createApp } from 'vue';

 //root component to list the routing parts
 const routes=[
    {path:'/',component:ChatBox},
    {path:'/upload',component:UploadPage},
]

const router = createRouter({
    history: createWebHistory(),
    routes, // short for `routes: routes`
})

const app = createApp(App);
app.use(router);

app.mount('#app');
  