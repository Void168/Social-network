<template>
  <div class="w-[50%] my-12 space-y-4 dark:text-neutral-200">
    <div class="dark:bg-slate-700 rounded-lg p-4">
      <div>
        <h3 class="text-lg font-semibold">
          Thành viên &middot; {{ group.members_count }}
        </h3>
        <h4 class="text-neutral-400">
          Người và Trang mới tham gia nhóm này sẽ hiển thị tại đây.
          <strong class="dark:text-neutral-200 hover:underline cursor-pointer"
            >Tìm hiểu thêm</strong
          >
        </h4>
        <div class="relative w-full">
          <MagnifyingGlassIcon
            class="absolute top-[18px] left-2 sm:w-6 sm:h-6 xs:w-3 xs:h-3 dark:text-neutral-400"
          />
          <input
            ref="input"
            type="text"
            placeholder="Tìm thành viên"
            class="w-full my-2 sm:py-2 sm:px-8 xs:py-1 xs:px-6 border border-gray-200 dark:bg-slate-800 dark:border-slate-800 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
          />
        </div>
      </div>
      <hr class="border my-4 dark:border-slate-600" />
      <div class="flex justify-between items-center px-4 py-2">
        <div class="flex items-center gap-2">
          <img
            :src="group?.admin?.get_avatar"
            alt="admin-avatar"
            class="w-16 h-16 rounded-full"
          />
          <div>
            <h3 class="font-semibold">{{ userStore.user.name }}</h3>
            <h4 class="text-sm">Làm việc tại</h4>
          </div>
        </div>
        <EllipsisHorizontalIcon
          class="w-8 rounded-lg dark:bg-slate-600 dark:hover:bg-slate-500 duration-75 font-medium cursor-pointer"
        />
      </div>
      <hr class="border my-4 dark:border-slate-600" />
      <div>
        <h3 class="text-lg font-semibold">
          Chủ nhóm & quản trị viên &middot;
          {{ 1 + group?.moderators?.length }}
        </h3>
        <div class="flex flex-col gap-2">
          <div class="flex justify-between items-center px-4 py-2">
            <div class="flex items-center gap-2">
              <img
                :src="group?.admin?.get_avatar"
                alt="admin-avatar"
                class="w-16 h-16 rounded-full"
              />
              <div>
                <h3 class="font-semibold">{{ group?.admin?.name }}</h3>
                <h4 class="text-sm">Chủ nhóm</h4>
              </div>
            </div>
          </div>
          <div class="flex items-center justify-between">
            <div
              v-for="moderator in group?.moderators"
              :key="moderator.id"
              class="px-4 py-2 flex items-center gap-2"
            >
              <img
                :src="moderator?.information?.get_avatar"
                alt="admin-avatar"
                class="w-16 h-16 rounded-full shadow-lg"
              />
              <div>
                <h3 class="font-semibold">
                  {{ moderator?.information?.name }}
                </h3>
                <h4 class="text-sm">Quản trị viên</h4>
              </div>
            </div>
            <button
              class="flex gap-2 items-center px-4 py-2 rounded-lg dark:bg-slate-800 dark:hover:bg-slate-600 duration-75 font-medium"
            >
              <UserPlusIcon class="w-6" />
              Thêm bạn bè
            </button>
          </div>
        </div>
      </div>
      <hr class="border my-4 dark:border-slate-600" />
      <div>
        <h3 class="text-lg font-semibold">
          Bạn bè &middot;
          {{ 1 + group?.moderators?.length }}
        </h3>
        <div class="flex flex-col px-4 py-2">
          <div
            v-for="friend in friends.slice(0, 3)"
            :key="friend.id"
            class="flex justify-between items-center px-4 py-2"
          >
            <RouterLink
              :to="{
                name: 'profile',
                params: { id: friend?.information?.id },
              }"
              class="flex items-center gap-2"
            >
              <img
                :src="friend?.information?.get_avatar"
                alt="admin-avatar"
                class="w-16 h-16 rounded-full"
              />
              <div>
                <h3 class="font-semibold">
                  {{ friend?.information?.name }}
                </h3>
                <h4 class="text-sm">Làm việc tại</h4>
              </div>
            </RouterLink>
            <button
              class="flex gap-2 items-center px-4 py-2 rounded-lg dark:bg-slate-800 dark:hover:bg-slate-600 duration-75 font-medium"
            >
              <ChatBubbleLeftEllipsisIcon class="w-6" />
              Nhắn tin
            </button>
          </div>
        </div>
        <button
          v-if="friends.length > 3"
          class="flex w-full items-center px-4 py-2 rounded-2xl dark:bg-slate-800 dark:hover:bg-slate-600 duration-75 font-medium justify-center mt-4"
        >
          Xem tất cả
        </button>
      </div>
      <hr class="border my-4 dark:border-slate-600" />
      <div>
        <h3 class="text-lg font-semibold">Thành viên ở gần bạn &middot; 10</h3>
        <div class="flex flex-col justify-between items-center px-4 py-2 gap-2">
          <div
            v-for="n in 3"
            :key="n"
            class="w-full flex justify-between items-center"
          >
            <RouterLink
              :to="{
                name: 'profile',
                params: { id: friends[0]?.information?.id },
              }"
              class="flex items-center gap-2"
            >
              <img
                :src="friends[0]?.information?.get_avatar"
                alt="admin-avatar"
                class="w-16 h-16 rounded-full"
              />
              <div>
                <h3 class="font-semibold">
                  {{ friends[0]?.information?.name }}
                </h3>
                <h4 class="text-sm">Làm việc tại</h4>
              </div>
            </RouterLink>
            <button
              class="flex gap-2 items-center px-4 py-2 rounded-lg dark:bg-slate-800 dark:hover:bg-slate-600 duration-75 font-medium"
            >
              <UserPlusIcon class="w-6" />
              Thêm bạn bè
            </button>
          </div>
        </div>
        <button
          class="flex w-full items-center px-4 py-2 rounded-2xl dark:bg-slate-800 dark:hover:bg-slate-600 duration-75 font-medium justify-center mt-4"
        >
          Xem tất cả
        </button>
      </div>
      <div class="my-4">
        <div class="my-4">
          <h3 class="text-lg font-semibold">Mới vào nhóm</h3>
          <h5 class="text-xs">
            Danh sách này bao gồm những người đã tham gia nhóm và những người
            đang xem trước nhóm. Bất kỳ người nào được mời và được phê duyệt đều
            có thể xem trước nội dung trong nhóm.
          </h5>
        </div>
        <div class="flex flex-col justify-between items-center px-4 py-2 gap-2">
          <div
            v-for="member in group.members"
            :key="member.id"
            class="w-full flex justify-between items-center"
          >
            <RouterLink
              :to="{
                name: 'profile',
                params: { id: member?.information?.id },
              }"
              class="flex items-center gap-2"
            >
              <img
                :src="member?.information?.get_avatar"
                alt="admin-avatar"
                class="w-16 h-16 rounded-full"
              />
              <div>
                <h3 class="font-semibold">
                  {{ member?.information?.name }}
                </h3>
                <h4 class="text-sm">Làm việc tại</h4>
              </div>
            </RouterLink>
            <GroupMemberDropdown :member="member" :group="group" @removeMember="removeMember"/>
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
  ClockIcon,
  AdjustmentsHorizontalIcon,
  ChevronDownIcon,
  MagnifyingGlassIcon,
  EllipsisHorizontalIcon,
  UserPlusIcon,
  ChatBubbleLeftEllipsisIcon,
} from "@heroicons/vue/24/solid";
import GroupDetailNavigation from "../../components/items/group/GroupDetailNavigation.vue";
import GroupHeader from "../../components/items/group/GroupHeader.vue";
import GroupMemberDropdown from "../../components/dropdown/GroupMemberDropdown.vue";

export default {
  name: "groupmembers",
  components: {
    ClockIcon,
    AdjustmentsHorizontalIcon,
    ChevronDownIcon,
    MagnifyingGlassIcon,
    EllipsisHorizontalIcon,
    UserPlusIcon,
    ChatBubbleLeftEllipsisIcon,
    RouterLink,
    GroupDetailNavigation,
    GroupHeader,
    GroupMemberDropdown,
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
      requests: [],
      isUserInGroup: false,
      friends: [],
    };
  },

  mounted() {
    this.checkUserInGroup();
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
          this.getFriendsInGroup();
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
          //   console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getFriendsInGroup() {
      await axios
        .get(`/api/group/${this.$route.params.id}/get-friends/`)
        .then((res) => {
          this.friends = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    removeMember(member){
      axios.post(`/api/group/${this.group.id}/kick/${member.id}/`).then((res) => {
        if(res.data.message){
          this.toastStore.showToast(
            3500,
            `Đã xóa ${member.name} khỏi nhóm.`,
            "bg-emerald-500 text-white"
          );
        }
      }).catch((error) => {
        console.log(error)
      })
    }
  },
};
</script>
