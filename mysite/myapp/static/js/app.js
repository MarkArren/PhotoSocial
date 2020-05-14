var postComponent = Vue.component("post", {
    props: ["post"],
    template: `
    <div class="post-container">
        <div class="post">
            <div class="post-image">
                <img :src="post.image" />
                <div class="post-caption">
                    <a :href="'/u/' + post.username" class="username">@{{ post.username }}</a><br>
                    <span v-if="post.location"><i data-feather="navigation" class="post-icon-white"></i>{{ post.location }}<br></span>
                    <span>{{ post.caption }}</span>
                </div>
            </div>
            <div class="post-item-bar">
                <div v-if="post.isOwnPost" v-on:click="onDelete()" class="post-button">
                    <i data-feather="x-circle" class="post-icon"></i>
                    <p>‎</p>
                </div>
                <a :href="'/u/' + post.username" class="post-button">
                    <i data-feather="user" class="post-icon"></i>
                    <p>‎</p>
                </a>
                <div v-on:click="onSubmitLike()" class="post-button">
                    <div v-show="post.liked">
                        <i data-feather="heart" class="post-icon fill-white"></i>
                    </div>
                    <div v-show="!post.liked">
                        <i data-feather="heart" class="post-icon"></i>
                    </div>
                    <p>{{ post.likeCount }}</p>
                </div>
                <div v-on:click="showComments = !showComments" class="post-button">
                    <i data-feather="message-circle" class="post-icon fill-white"></i>
                    <p>{{ post.commentCount }}</p>
                </div>
            </div>
        </div>

        <div class="comment-container" v-show="showComments">
            <div v-on:click="showComments = !showComments" class="comments-top-bar">
                <i data-feather="chevron-down" class="post-icon"></i>
            </div>
            <div class="comments">
                <div v-for="commentObjects in post.comments">
                    <div class="comment">
                        <div><img :src="commentObjects.comment.profilePicture" alt="profile"></div>
                        <div>
                            <a :href="'/u/' + commentObjects.comment.username"><span class="username">@{{ commentObjects.comment.username }}</span></a></br>
                            <span>{{ commentObjects.comment.comment }}</span></br>
                            <a v-on:click="parentComment = commentObjects.comment.id" class="reply">reply</a>
                        </div>
                        <div></div>
                    </div>

                    <div class="child-comments">
                        <div v-for="childComment in commentObjects.childComments" class="comment">
                            <div><img :src="childComment.profilePicture" alt="profile"></div>
                            <div>
                                <a :href="'/u/' + childComment.username"><span class="username">@{{ childComment.username }}</span></a></br>
                                <span>{{ childComment.comment }}</span>
                            </div>
                            <div></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="comment-form">
                <input v-bind:value="comment" v-on:input="comment = $event.target.value" placeholder="Add Comment..." type="text" name="comment">
                <div v-on:click="onSubmitComment"><i data-feather="send" class="post-icon"></i></button>
                </div>
            </div>
        </div>
    </div>
    `,
    data: function () {
        return {
            showComments: false,
            parentComment: "",
            comment: null
        }
    },
    methods: {
        onSubmitLike: function () {
            // Getting parameters
            const params = new URLSearchParams();
            params.append("post", this.post.id);
            params.append("csrfmiddlewaretoken", this.post.token);
            params.append("type", "like");

            // Setting self so I can call this inside of promise
            const self = this;
            axios
                .post('/', params)
                .then(function (response) {
                    // self.fetchPostList();
                    self.$emit('refresh');
                })
                .catch(error => { });

            // Update props locally
            if (this.post.liked)
                this.post.likes--;
            else
                this.post.likes++;
            this.post.liked = !this.post.liked
        },
        onSubmitComment: function () {
            // Getting parameters
            const params = new URLSearchParams();
            params.append("post", this.post.id);
            params.append("comment", this.comment); // TODO
            params.append("parentComment", this.parentComment); // TODO
            params.append("csrfmiddlewaretoken", this.post.token);
            params.append("type", "comment");

            // Setting self so I can call this inside of promise
            const self = this;
            axios
                .post('/', params)
                .then(function (response) {
                    // Tell parent to refresh
                    self.$emit('refresh');
                    
                })
                .catch(error => { });

            this.comment = ""
            this.parentComment = ""
        },
        onDelete: function () {
            // Getting parameters
            const params = new URLSearchParams();
            params.append("post", this.post.id);
            params.append("csrfmiddlewaretoken", this.post.token);
            params.append("type", "delete");

            // Setting self so I can call this inside of promise
            const self = this;
            axios
                .post('/', params)
                .then(function (response) {
                    // Tell parent to refresh
                    self.$emit('refresh');
                    // self.fetchPostList();
                })
                .catch(error => { });
        }

    },
    mounted() {
        this.$nextTick(function () {
            feather.replace();
            console.log("Feather replacing post");
            feather.replace();
            // setTimeout(function(){ feather.replace(); }, 100);
        })
    }
});