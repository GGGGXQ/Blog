<template>
    <div class=",ax-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">修改密码</h1>
                <p class="mb-6 text-gray-500">
                    保护您的账户安全从未如此简单。<br>
                    通过我们的更改密码界面，您可以快速、安全地更新您的登录密码。<br>
                    安全提示：<br>
                    请定期更换密码，以增强账户安全性。<br>
                    使用包含大小写字母、数字和特殊字符的复杂密码。<br>
                    避免使用容易猜到的信息，如生日、电话号码或常用词汇。
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6"  v-on:submit.prevent="submitForm">
                    <div>
                        <label>旧密码</label><br>
                        <input type="password" v-model="form.old_password" placeholder="请输入你的旧密码" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <div>
                        <label>新密码</label><br>
                        <input type="password" v-model="form.new_password1" placeholder="请输入你的新密码" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <div>
                        <label>再次输入新密码</label><br>
                        <input type="password" v-model="form.new_password2" placeholder="请再次输入你的新密码" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
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
                old_password: '',
                new_password1: '',
                new_password2: '',
            },
            errors: [],
        }
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.form.old_password === '') {
                this.errors.push('请输入旧密码')
            }

            if (this.form.new_password1 === '') {
                this.errors.push('请输入新密码')
            }

            if (this.form.new_password1 !== this.form.new_password2) {
                this.errors.push('两次密码不匹配！')
            }
            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('old_password', this.form.old_password)
                formData.append('new_password1', this.form.new_password1)
                formData.append('new_password2', this.form.new_password2)
                axios
                    .post('/api/editpassword/',  formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, '修改已保存', 'bg-emerald-500')

                            this.$router.push(`/profile/${this.userStore.user.id}`)
                        } else {
                            const data = JSON.parse(response.data.message)

                            for (const key in data){
                                this.errors.push(data[key][0].message)
                            }
                        }

                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    },
}   
</script>