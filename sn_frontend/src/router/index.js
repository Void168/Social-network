import { createRouter, createWebHistory } from "vue-router";
import SignUpView from "../views/SignUpView.vue";
import LoginView from "../views/LoginView.vue";
import FeedView from "../views/FeedView.vue";
import GroupView from "../views/GroupView.vue";
import SearchView from "../views/SearchView.vue";
import ProfileView from "../views/ProfileView.vue";
import ProfileImagesView from "../views/ProfileImagesView.vue";
import GroupDetailView from "../views/GroupDetailView.vue"
import FriendsView from "../views/FriendsView.vue";
import PostView from "../views/PostView.vue";
import PagePostView from "../views/PagePostView.vue";
import ChatView from "../views/ChatView.vue";
import GroupChatView from "../views/GroupChatView.vue";
import PageChatView from "../views/PageChatView.vue";
import TrendView from "../views/TrendView.vue";
import EditProfileView from "../views/EditProfileView.vue";
import EditPasswordView from "../views/EditPasswordView.vue";
import NotificationsView from "../views/NotificationsView.vue";
import ConversationView from "../views/ConversationView.vue";
import StoryView from "../views/StoryView.vue";
import PageView from "../views/PageView.vue"
import EditPageView from "../views/EditPageView.vue"
import PageUsersView from "../views/PageUsersView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/signup",
      name: "signup",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/",
      name: "feed",
      component: FeedView,
    },
    {
      path: "/groups",
      name: "group",
      component: GroupView,
    },
    {
      path: "/stories",
      name: "story",
      component: StoryView,
    },
    {
      path: "/search",
      name: "search",
      component: SearchView,
    },
    {
      path: "/chat",
      name: "chat",
      component: ChatView,
    },
    {
      path: "/notifications",
      name: "notifications",
      component: NotificationsView,
    },
    {
      path: "/trends/:id",
      name: "trendview",
      component: TrendView,
    },
    {
      path: "/profile/:id",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/page/:id",
      name: "page",
      component: PageView,
    },
    {
      path: "/group/:id",
      name: "groupdetail",
      component: GroupDetailView,
    },
    {
      path: "/page/:id/users",
      name: "pageusers",
      component: PageUsersView,
    },
    {
      path: "/page/edit",
      name: "pageEdit",
      component: EditPageView,
    },
    {
      path: "/chat/:id",
      name: "conversation",
      component: ConversationView,
    },
    {
      path: "/group-chat/:id",
      name: "groupConversation",
      component: GroupChatView,
    },
    {
      path: "/page-chat/:id",
      name: "pageConversation",
      component: PageChatView,
    },
    {
      path: "/profile/edit",
      name: "profileedit",
      component: EditProfileView,
    },
    {
      path: "/profile/edit/password",
      name: "editpassword",
      component: EditPasswordView,
    },
    {
      path: "/profile/:id/friends",
      name: "friends",
      component: FriendsView,
    },
    {
      path: "/profile/:id/photos",
      name: "photos",
      component: ProfileImagesView,
    },
    {
      path: "/post/:id",
      name: "postview",
      component: PostView,
    },
    {
      path: "/page/post/:id",
      name: "pagepostview",
      component: PagePostView,
    },
  ],
});

export default router;
