import { createRouter, createWebHistory } from "vue-router";
import SignUpView from "../views/auth/SignUpView.vue";
import LoginView from "../views/auth/LoginView.vue";
import FeedView from "../views/FeedView.vue";
import GroupView from "../views/group/GroupView.vue";
import SearchView from "../views/SearchView.vue";
import GroupSearchView from "../views/group/GroupSearchView.vue"
import GroupDetailView from "../views/group/GroupDetailView.vue";
import GroupDiscussView from "../views/group/GroupDiscussView.vue"
import GroupAboutView from "../views/group/GroupAboutView.vue";
import GroupMediaView from "../views/group/GroupMediaView.vue"
import GroupFileView from "../views/group/GroupFileView.vue"
import GroupQuestionView from "../views/group/manage/GroupQuestionView.vue"
import GroupPostView from "../views/group/GroupPostView.vue";
import GroupMembersView from "../views/group/GroupMembersView.vue";
import GroupJoinRequestView from "../views/group/manage/GroupJoinRequestView.vue";
import GroupPendingPostView from "../views/group/manage/GroupPendingPostView.vue"
import GroupRulesView from "../views/group/manage/GroupRulesView.vue"
import GroupEditView from "../views/group/manage/GroupEditView.vue"
import GroupOverviewView from "../views/group/manage/GroupOverviewView.vue"
import GroupGrowthView from "../views/group/manage/GroupGrowthView.vue"
import ProfileView from "../views/profile/ProfileView.vue";
import ProfileDetailView from "../views/profile/ProfileDetailView.vue"
import ProfileImagesView from "../views/profile/ProfileImagesView.vue";
import FriendsView from "../views/profile/FriendsView.vue";
import ProfileAboutView from "../views/profile/ProfileAboutView.vue"
import PostView from "../views/post/PostView.vue";
import PagePostView from "../views/page/PagePostView.vue";
import ChatView from "../views/chat/ChatView.vue";
import GroupChatView from "../views/chat/GroupChatView.vue";
import PageChatView from "../views/chat/PageChatView.vue";
import PageDetailView from "../views/page/PageDetailView.vue"
import TrendView from "../views/post/TrendView.vue";
import EditProfileView from "../views/profile/EditProfileView.vue";
import EditPasswordView from "../views/profile/EditPasswordView.vue";
import NotificationsView from "../views/NotificationsView.vue";
import ConversationView from "../views/chat/ConversationView.vue";
import StoryView from "../views/StoryView.vue";
import PageView from "../views/page/PageView.vue";
import EditPageView from "../views/page/EditPageView.vue";
import PageUsersView from "../views/page/PageUsersView.vue";
import PageAboutView from "../views/page/PageAboutView.vue"
import PageImageView from "../views/page/PageImageView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_CLIENT_URL),
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
      props: true,
      redirect: {name: "profiledetail"},
      children: [
        {
          path: "/profile/:id/",
          name: "profiledetail",
          component: ProfileDetailView,
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
          path: "/profile/:id/about",
          name: "about",
          component: ProfileAboutView,
        },
      ]
    },
    {
      path: "/page/:id",
      name: "page",
      component: PageView,
      props: true,
      redirect: {name: "pagedetail"},
      children: [
        {
          path: "/page/:id/",
          name: "pagedetail",
          component: PageDetailView,
        },
        {
          path: "/page/:id/users",
          name: "pageusers",
          component: PageUsersView,
        },
        {
          path: "/page/:id/about",
          name: "pageabout",
          component: PageAboutView,
        },
        {
          path: "/page/:id/photos",
          name: "pagephotos",
          component: PageImageView,
        },
      ]
    },
    {
      path: "/groups/:id",
      component: GroupDetailView,
      props: true,
      redirect: {name: "groupdiscuss"},
      name: 'groupdetail',
      children: [
        {
          path: "/groups/:id/",
          component: GroupDiscussView,
          name: "groupdiscuss",
        },
        {
          path: "about",
          component: GroupAboutView,
          name: "groupabout",
        },
        {
          path: "media",
          component: GroupMediaView,
          name: "groupmedia",
        },
        {
          path: "files",
          component: GroupFileView,
          name: "groupfile",
        },
        {
          path: "members",
          component: GroupMembersView,
          name: "groupmembers",
        },
        {
          path: "membership-questions",
          component: GroupQuestionView,
          name: "groupquestion",
        },
        {
          path: "member-request",
          component: GroupJoinRequestView,
          name: "groupjoinrequest",
        },
        {
          path: "pending-posts",
          component: GroupPendingPostView,
          name: "grouppendingpost",
        },
        {
          path: "edit",
          component: GroupEditView,
          name: "groupedit",
        },
        {
          path: "search",
          component: GroupSearchView,
          name: "groupsearch",
        },
        {
          path: "rules",
          component: GroupRulesView,
          name: "grouprules",
        },
        {
          path: "post/:postid",
          component: GroupPostView,
          name: "grouppost",
        },
        {
          path: "overview",
          component: GroupOverviewView,
          name: "groupoverview",
        },
        {
          path: "growth",
          component: GroupGrowthView,
          name: "groupgrowth",
        },
      ],
    },
    {
      path: "/page/post/:id",
      name: "pagepostview",
      component: PagePostView,
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
      path: "/post/:id",
      name: "postview",
      component: PostView,
    },
  ],
});

export default router;
