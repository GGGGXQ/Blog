<template>
    <form v-on:submit.prevent="submitForm" method="post">
        <div class="p-4">
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="此刻在想什么"></textarea>
            <div id="preview" v-if="url">
                <img :src="url" class="w-[100px] mt-3 rounded-xl" />
            </div>
        </div>
        <div class="p-4 border-t border-gray-100 flex justify-between">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg"><input type="file" ref="file" @change="onFileChange">附加照片</label>
            
            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">发布</button>
        </div>
    </form>
</template>

<script>
import axios from 'axios'

export default {
    props: {
        user: Object,
        posts: Array
    },

    data() {
        return {
            body: '',
            is_private: false,
            url: null,
        }
    },

    methods: {
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
        
        submitForm() {
            if (this.body==='' && this.url===null) {
                alert('不可发送空帖子')
                console.log('Body:', body); 
                console.log('URL:',url);
                return;
            }
            
            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    this.posts.unshift(response.data)
                    this.body = ''
                    this.$refs.file.value = null
                    this.url = null

                    if (this.user) {
                        this.user.posts_count += 1
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>