import "./assets/main.css";

import { createApp } from "vue";
import { useUserStore } from "./stores/user";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import axios from "axios";

axios.defaults.baseURL = import.meta.VITE_BASE_URL || "http://127.0.0.1:8000";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router, axios);

const userStore = useUserStore();

router.beforeEach((to, from) => {
  if (to.path !== "/login" && !userStore.user.isAuthenticated) {
    return "/login";
  }

  if (to.path === "/login" && userStore.user.isAuthenticated) {
    return "/";
  }

  if (to.path === "/signup" && userStore.user.isAuthenticated) {
    return "/";
  }
});

app.mount("#app");
