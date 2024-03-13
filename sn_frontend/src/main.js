import "./assets/main.css";

import { createApp } from "vue";
import { useUserStore } from "./stores/user";
import { usePageStore } from "./stores/page";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import axios from "axios";

axios.defaults.baseURL = import.meta.env.VITE_BASE_URL;

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router, axios);

const userStore = useUserStore();
const pageStore = usePageStore();

router.beforeEach((to, from, next) => {
  if (!userStore.user.isAuthenticated) {
    if (to.path !== "/auth/login" && to.path !== "/auth/signup") {
      next({ name: "login" });
    } else {
      next();
    }
  } else if (
    (to.path === "/auth/login" && userStore.user.isAuthenticated) ||
    (to.path === "/auth/signup" && userStore.user.isAuthenticated)
  ) {
    next({ name: "feed" });
  } else next();
});

app.mount("#app");
