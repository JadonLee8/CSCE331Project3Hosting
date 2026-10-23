<script lang="ts">
  let dbStatus: string = $state('')

  async function pingDb() {
    dbStatus = 'Checking...'
    try {
      const res = await fetch('/api/db-ping')
      const body = await res.json()
      dbStatus = body.status
    } catch (err) {
      dbStatus = `Backend unreachable: ${err}`
    }
  }
</script>

<h1>Landing Page</h1>
<p>Welcome to Dunsin's Donuts</p>

<button type="button" onclick={pingDb}>Test DB connection</button>
<p>{dbStatus}</p>
