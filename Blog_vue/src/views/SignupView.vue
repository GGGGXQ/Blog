<template>
    <div class=",ax-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">注册</h1>
                <p class="mb-6 text-gray-500">
                    创建个人账户，分享您的美好瞬间，记录生活中的点滴幸福。<br>
                    同时，您也可以便捷地浏览他人的精彩故事，参与互动，留下您的独到见解和评论。<br>
                    让我们共同构建一个充满活力和共鸣的社区。
                </p>

                <p class="font-bold">
                    已经有账号了？<RouterLink :to="{'name': 'login'}" class="underline">点击这里</RouterLink> 开始登录个人账号！
                </p>
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
                        <label>邮箱</label><br>
                        <input type="email" v-model="form.email" placeholder="你的邮箱" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <div>
                        <label>密码</label><br>
                        <input type="password" v-model="form.password1" placeholder="请输入密码" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <div>
                        <label>再次输入密码</label><br>
                        <input type="password" v-model="form.password2" placeholder="请再次输入密码" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">注册</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import { useToastStore } from '@/stores/toast'
import { userUserStore } from '@/stores/user'

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = userUserStore()

        return {
            toastStore,
            userStore
        }
    },

    data() {
        return {
            form: {
                email: '',
                name: '',
                password1: '',
                password2: ''
            },
            errors: [],
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

        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('请输入你的邮箱')
            }

            if (this.form.name === '') {
                this.errors.push('请输入你的昵称')
            }

            if (this.form.password1 === '') {
                this.errors.push('请输入密码')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('两次密码不匹配！')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/signup/', this.form)
                    .then(response => {
                        if (response.data.message === 'success') {  
                            this.toastStore.showToast(5000, '用户已注册!', 'bg-emerald-500')

                            this.form.email = ''
                            this.form.name = ''
                            this.form.password1 = ''
                            this.form.password2 = ''
                        } else {
                            const data = JSON.parse(response.data.message)
                            for (const key in data){
                                this.errors.push(data[key][0].message)
                            }

                            this.toastStore.showToast(5000, data[key][0].message, 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>