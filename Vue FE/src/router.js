// router.js
import { createRouter, createWebHistory } from "vue-router";
import ChatBox from "./components/ChatBox.vue";
import UploadPage from "./components/UploadPage.vue";

const routes = [
  { path: "/", component: ChatBox },
   { path: "/upload", component: UploadPage },
 
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
