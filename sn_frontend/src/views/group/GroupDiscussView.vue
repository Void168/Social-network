<template>
  <div class="w-full flex flex-col justify-center items-center">
    <div class="flex xl:w-[80%] w-full my-4 gap-4 px-4">
      <div class="lg:w-[60%] w-full " id="feed-frame">
        <div v-if="isUserInGroup" class="flex flex-col space-y-4">
          <div class="dark:bg-slate-700 bg-white rounded-lg px-4">
            <div class="py-4 flex items-start gap-2 p-2 rounded-lg">
              <div>
                <img
                loading="lazy"
                  :src="
                    isAnonymous
                      ? 'https://cdn-icons-png.flaticon.com/512/350/350351.png'
                      : currentMember?.information?.get_avatar
                  "
                  alt="member-avatar"
                  class="w-10 h-10 rounded-full"
                />
              </div>
              <GroupPollForm
                :group="group"
                v-if="isPollOpen"
                :isAnonymous="isAnonymous"
              />
              <textarea
                v-else
                v-model="body"
                class="p-4 w-full bg-gray-100 rounded-lg resize-none"
                cols="30"
                rows="4"
                placeholder="Bạn đang nghĩ gì?"
              ></textarea>
            </div>
            <div
              v-if="urlPost"
              class="flex relative justify-center items-center w-full p-4 border-[1px] border-slate-400 rounded-lg my-2"
            >
              <img loading="lazy" :src="urlPost" class="w-full rounded-lg" />
              <XCircleIcon
                class="absolute top-5 right-5 cursor-pointer w-10 h-10"
                @click="removeImage"
              >
              </XCircleIcon>
            </div>
            <hr class="mx-4 border dark:border-slate-600" />
            <div class="flex flex-wrap justify-center w-full items-center gap-2 px-4 py-2">
              <div
                @click="activateAnonymous"
                class="flex items-center font-medium justify-center gap-2 py-2 px-4  rounded-lg dark:hover:bg-slate-800 cursor-pointer duration-75"
                :class="isAnonymous ? 'dark:bg-slate-800 bg-slate-400' : ''"
                v-if="group.anonymous_post"
              >
              <span class="xm:text-base text-xs flex gap-2 cursor-pointer">
                <EyeSlashIcon class="w-6 text-sky-500" />
                Bài viết ẩn danh
              </span>
              </div>
              <div
                v-if="!isPollOpen"
                class="flex items-center font-medium justify-center gap-2 py-2 px-4 rounded-lg dark:hover:bg-slate-800 cursor-pointer duration-75"
              >
                <label for="doc">
                  <span class="xm:text-base text-xs flex gap-2 cursor-pointer"
                    ><PhotoIcon class="w-6 text-emerald-500" />Ảnh/Video</span
                  >
                  <input
                    type="file"
                    ref="file"
                    id="doc"
                    name="doc"
                    hidden
                    @change="onFileChange"
                  />
                </label>
              </div>
              <div
                class="flex items-center font-medium justify-center gap-2 py-2 px-4 rounded-lg dark:hover:bg-slate-800 cursor-pointer duration-75"
                :class="isPollOpen ? 'bg-slate-800' : ''"
                @click="createPollOpen"
                v-if="group.anyone_can_poll"
              >
              <span class="xm:text-base text-xs flex gap-2 cursor-pointer">
                <HandRaisedIcon class="w-6 text-amber-600" />
                Thăm dò ý kiến
              </span>
              </div>
            </div>
            <button
              @click="submitForm"
              class="w-full mb-4 font-semibold"
              :class="
                !body
                  ? 'dark:bg-slate-600 bg-slate-200 text-neutral-400 py-2 rounded-lg  duration-75'
                  : 'btn'
              "
              :disabled="!body"
              v-if="!isPollOpen"
            >
              Đăng bài viết
            </button>
          </div>
          <div class="flex items-center flex-wrap gap-2 justify-between">
            <div class="flex items-center gap-2 text-emerald-500 font-bold xm:text-base text-sm">
              Bài viết mới nhất
              <ChevronDownIcon class="w-5" />
            </div>
            <div class="flex gap-2 items-center">
              <div
                @click="togglePostTab"
                :class="
                  defaultTab ? 'bg-emerald-400' : 'dark:bg-slate-700 bg-white'
                "
                class="px-4 py-2 font-semibold rounded-lg hover:bg-emerald-600 duration-75 cursor-pointer xm:text-base text-xs"
              >
                Bài viết
              </div>
              <div
                @click="togglePollTab"
                :class="
                  !defaultTab ? 'bg-emerald-400' : 'dark:bg-slate-700 bg-white'
                "
                class="px-4 py-2 font-semibold rounded-lg dark:hover:bg-emerald-600 duration-75 cursor-pointer xm:text-base text-xs"
              >
                Cuộc thảo luận
              </div>
            </div>
          </div>
          <div
            class="dark:bg-slate-700 rounded-lg px-4 h-80 flex flex-col justify-center items-center"
            v-if="
              (!groupPosts?.length && defaultTab) ||
              groupStore.setDefaultTab === 1
            "
          >
            <h2 class="text-xl font-semibold">Nhóm chưa có bài viết nào.</h2>
            <h3 class="text-lg font-semibold">
              Hãy đăng bài để cùng nhau thảo luận nhé.
            </h3>
          </div>
          <div
            v-else-if="
              (groupPosts?.length && defaultTab) ||
              groupStore.setDefaultTab === 1
            "
          >
            <SkeletonLoadingPost v-if="isLoading" />
            <div v-else>
              <div
                class="dark:bg-slate-700 bg-white rounded-lg px-4"
                v-for="groupPost in groupPosts"
                :key="groupPost.id"
              >
                <GroupPost
                  :post="groupPost"
                  :group="group"
                />
              </div>
              <SkeletonLoadingPost
                v-if="allPosts.length !== groupPosts.length"
                v-show="!loadMore"
              />

              <div v-else class="flex justify-center items-center h-48">
                <p class="text-xl font-semibold">Đã tải hết bài viết</p>
              </div>
            </div>
          </div>
          <div
            class="dark:bg-slate-700 rounded-lg px-4"
            v-else-if="
              (polls?.length && !defaultTab) || groupStore.setDefaultTab === 2
            "
            v-for="poll in polls"
            :key="poll.id"
          >
            <GroupPostPoll
              :key="updateKey"
              :poll="poll"
              :group="group"
              :currentMember="currentMember"
            />
          </div>
          <div
            class="dark:bg-slate-700 rounded-lg px-4 h-80 flex flex-col justify-center items-center"
            v-else-if="
              (!polls?.length && !defaultTab) || groupStore.setDefaultTab === 2
            "
          >
            <h2 class="text-xl font-semibold">Nhóm chưa cuộc thảo luận nào.</h2>
            <h3 class="text-lg font-semibold">
              Hãy tạo cuộc thăm dò ý kiến để cùng nhau thảo luận nhé.
            </h3>
          </div>
        </div>
        <div
          v-else-if="!isUserInGroup && group.is_private_group"
          class="flex flex-col justify-center items-center dark:bg-slate-700 h-[500px] rounded-lg"
        >
          <img
          loading="lazy"
            src="https://th.bing.com/th/id/R.0b658885df48a3649d297aa3cb9b701c?rik=O%2bnowdCCiEHMBw&riu=http%3a%2f%2fwww.freeiconspng.com%2fuploads%2fyellow-lock-icon-1.png&ehk=vmtKzvuDRyuDCuxWRt5bkcNNyst9WtJzTsByLmk4QOI%3d&risl=&pid=ImgRaw&r=0"
            alt="lock"
            class="w-40 h-40 shadow-none"
          />
          <h2 class="font-bold text-xl dark:text-neutral-300">
            Đây là nhóm riêng tư
          </h2>
          <h3 class="text-lg dark:text-neutral-400">
            Hãy tham gia nhóm này để xem hoặc cùng thảo luận nhé.
          </h3>
        </div>
        <div v-else-if="!isUserInGroup && !group.is_private_group">
          <div
            class="dark:bg-slate-700 rounded-lg px-4 h-80 flex flex-col justify-center items-center"
          >
            <h2 class="text-xl font-semibold">Nhóm chưa có bài viết nào.</h2>
          </div>
        </div>
      </div>
      <div
        class="w-[40%] sticky space-y-4 lg:block hidden"
        :class="isUserInGroup ? 'overflow-y-scroll' : ''"
        :style="{
          height: `${toastStore.height}px`,
          top: `${toastStore.navbarHeight}px`,
        }"
      >
        <div
          class="dark:bg-slate-700 bg-white rounded-lg p-4 relative"
          v-if="
            isUserInGroup &&
            group?.admin?.id === userStore.user.id &&
            isSettingOpen &&
            step < 4
          "
        >
          <XMarkIcon class="w-6 top-4 right-4 absolute" @click="closeSetting" />
          <h3 class="font-semibold text-lg">
            Hãy hoàn tất quy trình thiết lập nhóm
          </h3>
          <h4 class="font-semibold">
            Đã hoàn thành
            <span class="text-emerald-400">{{ step }}/4</span> bước
          </h4>
          <h4 class="text-neutral-400">
            Tiếp tục thêm các thông tin chính và bắt đầu tương tác với cộng đồng
            của bạn.
          </h4>
          <hr class="border m-4 dark:border-slate-600" />
          <div class="flex flex-col w-full">
            <div
              class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg"
            >
              <UserIcon class="w-8 rounded-full p-1 dark:bg-slate-600 bg-slate-200" />
              <h3 class="text-lg">Mời mọi người tham gia</h3>
            </div>
            <div
              class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg"
              :class="
                group.get_cover_image !==
                'https://th.bing.com/th/id/OIP.o1n4kgruF-5cDCCx7jNYKQHaEo?pid=ImgDet&rs=1'
                  ? 'text-emerald-400'
                  : ''
              "
            >
              <PhotoIcon class="w-8 rounded-full p-1 dark:bg-slate-600 bg-slate-200" />
              <h3 class="text-lg">Thêm ảnh bìa</h3>
            </div>
            <div
              class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg"
              :class="group.biography !== '' ? 'text-emerald-400' : ''"
            >
              <PencilIcon class="w-8 rounded-full p-1 dark:bg-slate-600 bg-slate-200" />
              <h3 class="text-lg">Thêm phần mô tả</h3>
            </div>
            <div
              class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg"
              :class="groupPosts ? 'text-emerald-400' : ''"
            >
              <PencilSquareIcon class="w-8 rounded-full p-1 dark:bg-slate-600 bg-slate-200" />
              <h3 class="text-lg">Tạo bài viết</h3>
            </div>
          </div>
        </div>
        <div class="dark:bg-slate-700 bg-white rounded-lg p-4">
          <h2 class="text-xl font-bold">Giới thiệu</h2>
          <div class="flex gap-2" v-if="!group?.is_private_group">
            <div class="flex flex-col justify-start">
              <GlobeAsiaAustraliaIcon class="w-6" />
            </div>
            <div>
              <h3 class="font-semibold">Công khai</h3>
              <h4>
                Bất kỳ ai cũng có thể nhìn thấy mọi người trong nhóm và những gì
                họ đăng.
              </h4>
            </div>
          </div>
          <div class="flex gap-2" v-else>
            <div class="flex flex-col justify-start">
              <LockClosedIcon class="w-6" />
            </div>
            <div>
              <h3 class="font-semibold">Riêng tư</h3>
              <h4>
                Chỉ thành viên mới nhìn thấy mọi người trong nhóm và những gì họ
                đăng.
              </h4>
            </div>
          </div>
          <div class="flex gap-2">
            <div class="flex flex-col justify-start" v-if="group?.show_group">
              <EyeIcon class="w-6" />
            </div>
            <div class="flex flex-col justify-start" v-else>
              <EyeSlashIcon class="w-6" />
            </div>
            <div v-if="group?.show_group">
              <h3 class="font-semibold">Hiển thị</h3>
              <h4>Ai cũng có thể tìm thấy nhóm này.</h4>
            </div>
            <div v-else>
              <h3 class="font-semibold">Ẩn</h3>
              <h4>Chỉ thành viên mới tìm thấy nhóm này.</h4>
            </div>
          </div>
        </div>
        <div class="dark:bg-slate-700 bg-white rounded-lg p-4 space-y-2" v-if="isUserInGroup">
          <h3 class="font-semibold text-lg">File phương tiện mới đây</h3>
          <div
            v-for="image in groupImages?.slice(0, 4)"
            :key="image.id"
            class="grid grid-cols-2"
          >
            <GroupImageShowcase
              :groupPost="image"
              :index="groupImages.indexOf(image)"
            />
          </div>
          <div
            v-if="groupImages.length"
            class="w-full flex justify-center items-center rounded-lg py-2 dark:bg-slate-600 cursor-pointer dark:hover:bg-slate-500 bg-slate-200 hover:bg-slate-300 duration-75"
          >
            <RouterLink
              :to="{ name: 'groupmedia', params: { id: group.id } }"
              class="font-semibold"
            >
              Xem tất cả
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { useGroupStore } from "../../stores/group";
import { RouterLink } from "vue-router";

import GroupHeader from "../../components/items/group/GroupHeader.vue";
import GroupPost from "../../components/items/post/GroupPost.vue";
import GroupPostPoll from "../../components/items/group/poll/GroupPostPoll.vue";
import GroupImageShowcase from "../../components/items/group/GroupImageShowcase.vue";
import GroupPollForm from "../../components/forms/GroupPollForm.vue";
import SkeletonLoadingPost from "../../components/loadings/SkeletonLoadingPost.vue";

import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  EyeSlashIcon,
  PhotoIcon,
  HandRaisedIcon,
  XMarkIcon,
  XCircleIcon,
  UserIcon,
  PencilIcon,
  PencilSquareIcon,
  EyeIcon,
  ChevronDownIcon,
} from "@heroicons/vue/24/solid";
export default {
  name: "groupdiscuss",
  components: {
    RouterLink,
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    GroupHeader,
    EyeSlashIcon,
    PhotoIcon,
    HandRaisedIcon,
    XMarkIcon,
    XCircleIcon,
    UserIcon,
    PencilIcon,
    PencilSquareIcon,
    EyeIcon,
    ChevronDownIcon,
    GroupPost,
    GroupImageShowcase,
    GroupPollForm,
    GroupPostPoll,
    SkeletonLoadingPost,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const groupStore = useGroupStore();

    return {
      userStore,
      toastStore,
      groupStore,
    };
  },
  props: {
    group: Object,
    isUserInGroup: Boolean,
    currentMember: Object,
  },
  data() {
    return {
      body: "",
      step: 0,
      urlPost: null,
      groupPosts: [],
      allPosts: [],
      groupImages: [],
      polls: [],
      isAnonymous: false,
      isSettingOpen: true,
      isPollOpen: false,
      defaultTab: true,
      updateKey: 0,
      loadMore: false,
      PostToShow: 5,
      isLoading: false,
    };
  },

  mounted() {
    this.getGroupPostsList();
    this.getGroupImage();
    this.getSteps();
    this.getGroupPostPollsList();
    window.addEventListener("scroll", this.infinateScroll);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.infinateScroll);
  },

  methods: {
    forceUpdate() {
      this.updateKey += 1;
    },
    togglePostTab() {
      this.defaultTab = true;
      this.groupStore.setDefaultTab(1);
    },
    togglePollTab() {
      this.defaultTab = false;
      this.groupStore.setDefaultTab(2);
    },
    getSteps() {
      setTimeout(() => {
        if (this.group.biography !== "") {
          this.step += 1;
        }
        if (
          this.group.get_cover_image !==
          "https://th.bing.com/th/id/OIP.o1n4kgruF-5cDCCx7jNYKQHaEo?pid=ImgDet&rs=1"
        ) {
          this.step += 1;
        }
        if (this.groupPosts) {
          this.step += 1;
        }
      }, 500);
    },
    closeSetting() {
      this.isSettingOpen = false;
    },
    activateAnonymous() {
      this.isAnonymous = !this.isAnonymous;
    },
    createPollOpen() {
      this.isPollOpen = !this.isPollOpen;
    },
    removeImage() {
      this.urlPost = null;
    },
    onFileChange(e) {
      const file = e.target.files[0];
      this.urlPost = URL.createObjectURL(file);
    },
    async getGroupPostsList() {
      this.isLoading = true;
      await axios
        .get(`/api/posts/group/${this.$route.params.id}/`)
        .then((res) => {
          const publicPosts = res.data.publicPosts;
          const anonymousPosts = res.data.anonymousPosts;
          this.allPosts = publicPosts?.concat(anonymousPosts);
          this.groupPosts = this.allPosts?.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
          );
          this.groupPosts = this.allPosts?.slice(0, this.PostToShow);

          this.isLoading = false;
          // console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getGroupPostPollsList() {
      await axios
        .get(`/api/posts/group/${this.$route.params.id}/poll/`)
        .then((res) => {
          this.polls = res.data;
          // console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getGroupImage() {
      await axios
        .get(`/api/posts/group/${this.$route.params.id}/attachments/`)
        .then((res) => {
          this.groupImages = res.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    submitForm() {
      let formData = new FormData();
      formData.append("image", this.$refs.file.files[0]);
      formData.append("body", this.body);
      formData.append("is_anonymous", this.isAnonymous);

      axios
        .post(`/api/posts/create/group/${this.group.id}/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          // console.log("data", res.data);
          this.body = "";
          this.isAnonymous = false;
          this.$refs.file.value = null;
          this.urlPost = null;
          if (!this.group.pending_post) {
            this.groupPosts?.unshift(res.data);
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    infinateScroll() {
      const frame = document.getElementById("feed-frame");
      let height = frame.scrollHeight;
      let scrollY = window.scrollY;

      if (height < scrollY + 1000) {
        setTimeout(() => {
          this.loadMore = true;
        }, 1000);
        if (this.loadMore) {
          const newPosts = this.allPosts?.slice(
            this.groupPosts.length,
            this.groupPosts.length + this.PostToShow
          );
          this.groupPosts.push(...newPosts);
        }
      } else {
        this.loadMore = false;
      }
    },
  },
};
</script>
