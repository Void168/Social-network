<template>
  <div class="w-full flex flex-col justify-center items-center">
    <div class="w-[50%] my-12 space-y-4 dark:text-neutral-200">
      <div class="dark:bg-slate-700 rounded-lg p-4">
        <h3 class="font-semibold text-lg">Giới thiệu về nhóm này</h3>
        <hr class="border my-6 border-slate-600" />
        <h4>{{ group?.biography }}</h4>
        <div class="flex gap-2" v-if="group.is_private_group">
          <div class="flex flex-col justify-start">
            <GlobeAsiaAustraliaIcon class="w-6 py-1" />
          </div>
          <div>
            <h3 class="font-semibold text-lg">Công khai</h3>
            <h4>
              Bất kỳ ai cũng có thể nhìn thấy mọi người trong nhóm và những gì
              họ đăng.
            </h4>
          </div>
        </div>
        <div class="flex gap-2" v-else>
          <div class="flex flex-col justify-start">
            <LockClosedIcon class="w-6 py-1" />
          </div>
          <div>
            <h3 class="font-semibold text-lg">Riêng tư</h3>
            <h5 class="text-sm">
              Chỉ thành viên mới nhìn thấy mọi người trong nhóm và những gì họ
              đăng.
            </h5>
          </div>
        </div>
        <div class="flex gap-2">
          <div class="flex flex-col justify-start py-1" v-if="group.show_group">
            <EyeIcon class="w-6" />
          </div>
          <div class="flex flex-col justify-start py-1" v-else>
            <EyeSlashIcon class="w-6" />
          </div>
          <div v-if="group.show_group">
            <h3 class="font-semibold text-lg">Hiển thị</h3>
            <h5 class="text-sm">Ai cũng có thể tìm thấy nhóm này.</h5>
          </div>
          <div v-else>
            <h3 class="font-semibold">Ẩn</h3>
            <h4>Chỉ thành viên mới tìm thấy nhóm này.</h4>
          </div>
        </div>
        <div class="flex gap-2">
          <div class="flex flex-col justify-start py-1">
            <ClockIcon class="w-6" />
          </div>
          <div>
            <h3 class="font-semibold text-lg">Lịch sử</h3>
            <h5 class="text-sm">
              Đã tạo nhóm vào
              {{ group?.created_at?.slice(8, 10) }} tháng
              {{ group?.created_at?.slice(5, 7) }},
              {{ group?.created_at?.slice(0, 4) }}. Lần gần nhất đổi tên là vào
              18 tháng 2, 2022.
              <strong class="hover:underline cursor-pointer">Xem thêm</strong>
            </h5>
          </div>
        </div>
      </div>
      <div class="dark:bg-slate-700 rounded-lg p-4">
        <h3 class="font-semibold text-lg">
          Thành viên &middot; {{ group.members_count }}
        </h3>
        <hr class="border my-6 border-slate-600" />
        <div class="flex gap-1 items-center">
          <img
            :src="group?.admin?.get_avatar"
            alt="admin-avatar"
            class="w-8 h-8 rounded-full shadow-lg"
          />
          <div v-for="moderator in group?.moderators" :key="moderator.id">
            <img
              :src="moderator?.information?.get_avatar"
              alt="admin-avatar"
              class="w-8 h-8 rounded-full shadow-lg"
            />
          </div>
        </div>
        <div class="flex gap-1 my-2">
          <h4>{{ group?.admin?.name }} là chủ nhóm</h4>
          <h4 v-if="group?.moderators?.length">
            {{ group?.moderators[0]?.name }} và
            {{ group?.moderators?.length }} người khác nữa là quản trị viên
          </h4>
        </div>
      </div>
      <div class="dark:bg-slate-700 rounded-lg p-4 space-y-4">
        <h3 class="font-semibold text-lg">Hoạt động</h3>
        <hr class="border my-6 border-slate-600" />
        <div class="flex gap-2">
          <div class="flex flex-col justify-start py-1">
            <ChatBubbleBottomCenterTextIcon class="w-6" />
          </div>
          <div>
            <h4>Hôm nay có 0 bài viết mới</h4>
            <h5 class="text-sm">0 trong tháng trước</h5>
          </div>
        </div>
        <div class="flex gap-2">
          <div class="flex flex-col justify-start py-1">
            <UsersIcon class="w-6" />
          </div>
          <div>
            <h4>Tổng cộng {{ group.members_count }} thành viên</h4>
            <h5 class="text-sm">+ 0 trong tuần qua</h5>
          </div>
        </div>
        <div class="flex gap-2">
          <UserGroupIcon class="w-6" />
          <h4>Ngày tạo: {{ group?.created_at_formatted }} trước</h4>
        </div>
      </div>
      <div
        class="dark:bg-slate-700 rounded-lg p-4 space-y-4"
        v-if="rules.length"
      >
        <h3 class="text-lg font-semibold">Quy tắc nhóm của quản trị viên</h3>
        <hr class="my-4 border dark:border-slate-600" />
        <div v-for="rule in rules" :key="rule.id" class="flex gap-4">
          <div>
            <div class="flex gap-4">
              <span class="font-semibold">
                {{ rules.indexOf(rule) + 1 }}
              </span>
              <div class="flex flex-col space-y-2">
                <h3 class="font-semibold">{{ rule.name }}</h3>
                <h5 class="text-sm text-neutral-400">{{ rule.body }}</h5>
              </div>
            </div>
            <hr class="my-4 border dark:border-slate-600" />
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
import { RouterLink } from "vue-router";
import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  HomeIcon,
  EyeSlashIcon,
  EyeIcon,
  ClockIcon,
  ChatBubbleBottomCenterTextIcon,
  UserIcon,
  UserGroupIcon,
  UsersIcon,
} from "@heroicons/vue/24/solid";

export default {
  name: "groupabout",
  components: {
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    HomeIcon,
    EyeSlashIcon,
    EyeIcon,
    ClockIcon,
    ChatBubbleBottomCenterTextIcon,
    UserIcon,
    UserGroupIcon,
    RouterLink,
    UsersIcon,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  data() {
    return {
      group: {},
      isUserInGroup: false,
      rules: [],
    };
  },

  mounted() {
    this.checkUserInGroup();
    this.getRules();
  },

  methods: {
    async checkUserInGroup() {
      await axios
        .get(`/api/group/check-user/${this.$route.params.id}`)
        .then((res) => {
          if (res.data.message === "User joined the group") {
            this.isUserInGroup = true;
          } else {
            this.isUserInGroup = false;
          }
          this.getGroupDetail();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getGroupDetail() {
      await axios
        .get(`/api/group/${this.$route.params.id}/`)
        .then((res) => {
          this.group = res.data;
          // console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getRules() {
      axios
        .get(`/api/group/${this.$route.params.id}/get-rules/`)
        .then((res) => {
          this.rules = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
