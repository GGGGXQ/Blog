<template>
    <div class=",ax-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">登录</h1>
                <p class="mb-6 text-gray-500">
                    登录个人账号发表自己的文章，记录自己美好生活<br/>
                    同时更好地使用7+chat查看他人文章以及评论他人文章
                </p>

                <p class="font-bold">
                    没有账号了？<RouterLink :to= "{'name': 'signup'}" class="underline">点击这里</RouterLink> 开始创建个人账号！
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6">
                    <div>
                        <label>昵称</label><br>
                        <input type="text" placeholder="你的昵称" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <div>
                        <label>邮箱</label><br>
                        <input type="email" placeholder="你的邮箱" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <div>
                        <label>密码</label><br>
                        <input type="password" placeholder="请输入密码" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
                    </div>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-whit rounded-lg">登录</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>