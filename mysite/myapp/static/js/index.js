var posts = new Vue({
    el: '.posts',
    data: {
        posts: [],
        seen: true,
        unseen: false,
        empty: true
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
                .then(response => {
                    this.posts = response.data.posts;
                    if (this.posts.length > 0)
                        this.empty = false
                })
			this.seen = false
			this.unseen = true
            console.log("Refreshing main page")
        },
        cancelAutoUpdate: function(){ clearInterval(this.timer) },
    },
    beforeDestroy() {
		this.cancelAutoUpdate();
	},
	//mounted() {
	//	this. $nextTick(function () {
	//		feather.replace();
	//		console.log("mounted");
	//		setTimeout(function(){ feather.replace(); }, 100);
	//	})
	//}
	// components: {postComponent}
})
