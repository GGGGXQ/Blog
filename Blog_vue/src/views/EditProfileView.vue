<template>
    <div class=",ax-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">修改个人信息</h1>
                <p class="mb-6 text-gray-500">
                    管理您的个人信息，打造独特的数字身份。<br>
                    在这里，您可以轻松更新个人资料，确保您的信息准确无误，反映您的真实自我。<br>
                    通过个性化设置，您可以更自如地发表文章，记录和分享您的生活点滴。<br>
                    让我们共同构建一个充满活力的社区，让每个人都能在这里找到归属感。<br>

                </p>
                <RouterLink to="/profile/edit/password"><button class="py-4 px-6 bg-blue-600 text-white rounded-lg">修改密码</button></RouterLink>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6"  v-on:submit.prevent="submitForm">
                    <div>
                        <label>昵称</label><br>
                        <input type="text" v-model="form.name" placeholder="你的昵称" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <div>
                        <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg"><input type="file" ref="file" @change="onFileChange">修改头像</label>
                    </div>

                    <div id="preview" v-if="url">
                        <img :src="url" class="rounded-full object-cover w-24 h-24 sm:w-36 sm:h-36 mx-auto mb-6" />
                    </div>
                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">修改</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { userUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
    setup() {
        const userStore = userUserStore()
        const toastStore = useToastStore()

        return {
            toastStore,
            userStore,
        }
    },
    data() {
        return {
            form: {
                name: this.userStore.user.name,
            },
            errors: [],
            url: null,
        }
    },
    methods: {
        submitForm() {
            this.errors = []
            if (this.form.name === '') {
                this.errors.push('请输入你的昵称')
            }
            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('avatar', this.$refs.file.files[0])
                formData.append('name', this.form.name)
                axios
                    .post('/api/editprofile/',  formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.status===200) {  
                            this.toastStore.showToast(5000, '修改已保存', 'bg-emerald-500')
                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                avatar: response.data.user.get_avatar
                            })
                            this.url = null
                            this.$router.back()
                        } else {
                            this.toastStore.showToast(5000, '出错了，请重试！', 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        },

        onFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                if (!file.type.startsWith("image/")) {
                    alert("请上传图片文件！");
                    return;
                }
                this.url = URL.createObjectURL(file);
            } else {
                this.url = null;
            }
        },

    },
}   
</script>