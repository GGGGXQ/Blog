<template>
    <div class=",ax-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">登录</h1>
                <p class="mb-6 text-gray-500">
                    登录您的个人账号，开始撰写并发布您的文章，捕捉并珍藏生活中的美好瞬间。<br>
                    同时，您也能更便捷地阅读他人的精彩作品，参与讨论，分享您的见解和评论，<br>
                    与他人的文章互动，共同营造一个充满活力和深度的交流平台。
                </p>

                <p class="font-bold">
                    没有账号？<RouterLink :to= "{'name': 'signup'}" class="underline">点击这里</RouterLink> 开始创建个人账号！
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>邮箱</label><br>
                        <input type="email" v-model="form.email" placeholder="你的邮箱" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <div>
                        <label>密码</label><br>
                        <input type="password" v-model="form.password" placeholder="请输入密码" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">登录</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import { userUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = userUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: []
        }
    },

    mounted() {
        this.getStatus()
    },

    methods: {
        getStatus() {
            if (this.userStore.user.isAuthenticated) {
                this.$router.push('/feed')
            }
        }, 
        async submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('请输入邮箱')
            }

            if (this.form.password === '') {
                this.errors.push('请输入密码')
            }

            if (this.errors.length === 0) {
                await axios
                    .post('/api/login/', this.form)
                    .then(response => {
                        this.userStore.setToken(response.data)

                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
                    })
                    .catch(error => {
                        console.log('error', error)

                        this.errors.push('请检查邮箱或者密码是否正确，或不存在该用户!')
                    })
            }
            
            if (this.errors.length === 0) {
                await axios
                    .get('/api/me/')
                    .then(response => {
                        this.userStore.setUserInfo(response.data)

                        this.$router.push('/feed')
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>