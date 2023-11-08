<script>
    export let data;
    let username;
</script>
<label for="username">Username:</label>
<input type="text" id="username" name="username" bind:value={username}/>
<a href="/@/{username}">User data</a>
<p>{data.user_count}</p>