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
              <form v-on:submit.prevent="onDelete()" action="/" method="post">
                  <input type="hidden" name="post" :value="post.id">
                  <input type="hidden" name="csrfmiddlewaretoken" :value="post.token">
                  <button v-if="post.isOwnPost" type="submit" class="post-button">
                      <i data-feather="x-circle" class="post-icon"></i>
                      <p>‎</p>
                  </button>
              </form>
              <a :href="'/u/' + post.username">
                  <i data-feather="user" class="post-icon"></i>
                  <p>‎</p>
              </a>
              <form v-on:submit.prevent="onSubmitLike($event)" action="/" method="post">
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
    `,
    methods:{
        onSubmitLike: function (submitEvent) {
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
        onSubmitComment: function (submitEvent) {
			// Getting parameters
			const params = new URLSearchParams();
            params.append("postID", this.post.id);
            params.append("parentCommentID", submitEvent.target.elements.parentCommentID.value); // TODO
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
		this. $nextTick(function () {
			feather.replace();
            console.log("Feather replacing post");
            feather.replace();
			// setTimeout(function(){ feather.replace(); }, 100);
		})
	}
});