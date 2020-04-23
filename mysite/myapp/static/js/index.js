var postComponent = Vue.component("post", {
  props: ["post"],
  template: `
	<div class="post">
		<div class="post-image">
			<img :src="post.image" />
			<div class="post-caption">
				<a :href="'/u/' + post.username" class="username">@{{ post.username }}</a><br>
				<span>{{ post.caption }}</span>
      </div>
		</div>
		<div class="post-item-bar">
			<a :href="'/u/' + post.username">
				<i data-feather="user" class="post-icon"></i>
				<p>‎</p>
			</a>
			<form v-on:submit.prevent="$emit('liked', $event)" action="/" method="post">
				<input type="hidden" name="post" :value="post.id">
				<input type="hidden" name="csrfmiddlewaretoken" :value="post.token">
				<button v-show="post.liked" type="submit" class="post-button">
					<i data-feather="heart" class="post-icon fill-white"></i>
					<p>{{ post.likes }}</p>
				</button>
				<button v-show="!post.liked" type="submit" class="post-button">
					<i data-feather="heart" class="post-icon"></i>
					<p>{{ post.likes }}</p>
				</button>
			</form>
			<button type="submit" class="post-button">
				<i data-feather="message-circle" class="post-icon fill-white"></i>
				<p>{{ post.comments }}</p>
			</button>
		</div>
	</div>
  `
});

var posts = new Vue({
    el: '.posts',
    data: {
        posts: [],
        seen: true,
        unseen: false,
    },
    // Adapted from https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
    created: function(){
        this.fetchPostList();
        this.timer = setInterval(this.fetchPostList, 10000);
    },
    methods:{
        fetchPostList: function(){
            axios
				.get('/posts/')
                .then(response => (this.posts = response.data.posts))
			this.seen = false
            this.unseen = true
        },
        cancelAutoUpdate: function(){ clearInterval(this.timer) },
        // Sends post request to server to like post and refreshes posts
		onSubmitLike: function (submitEvent) {
			// Getting parameters
			const params = new URLSearchParams();
			params.append("post", submitEvent.target.elements.post.value);
			params.append("csrfmiddlewaretoken", submitEvent.target.elements.csrfmiddlewaretoken.value);
			params.append("type", "like");

			// Setting self so I can call this inside of promise
			const self = this;
			axios
				.post('/', params)
				.then(function (response) {
					self.fetchPostList();
				})
				.catch(error => { });
        },
        onSubmitComment: function (submitEvent) {
			// Getting parameters
			const params = new URLSearchParams();
            params.append("postID", submitEvent.target.elements.postID.value);
            params.append("parentCommentID", submitEvent.target.elements.parentCommentID.value);
			params.append("csrfmiddlewaretoken", submitEvent.target.elements.csrfmiddlewaretoken.value);
            params.append("type", "comment");

			// Setting self so I can call this inside of promise
			const self = this;
			axios
				.post('/', params)
				.then(function (response) {
					self.fetchPostList();
				})
				.catch(error => { });
		}
    },
    beforeDestroy() {
		this.cancelAutoUpdate();
	},
	// components: {postComponent}
})
