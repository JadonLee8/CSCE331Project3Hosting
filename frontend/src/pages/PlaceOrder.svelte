<script lang="ts">
  type MenuItem = {
    menu_item_id: number
    menu_item_name: string
    price: number
    category?: string
  }

  let menuItems: MenuItem[] = $state([])
  let selectedCategory: string = $state('All')

  let categories = $derived([
    'All',
    ...new Set(menuItems.map((item) => item.category ?? 'Other')),
  ])

  let visibleItems = $derived(
    selectedCategory === 'All'
      ? menuItems
      : menuItems.filter((item) => (item.category ?? 'Other') === selectedCategory)
  )

  async function fetchMenuItems() {
    try {
      const menuItemsResponse = await fetch('/api/menu-items')
      menuItems = await menuItemsResponse.json()
    } catch (err) {
      console.error('Error fetching menu items:', err)
    }
  }

  $effect(() => {
    fetchMenuItems()
  })
</script>

<div class="place-order flex min-h-0 flex-1">
  <aside class="flex w-[200px] flex-col gap-2 border-r border-line py-4 pr-4">
    {#each categories as category}
      <button
        type="button"
        class={[
          'btn text-left',
          category === selectedCategory &&
            'border-primary-dark bg-primary text-white hover:bg-primary',
        ]}
        onclick={() => (selectedCategory = category)}
      >
        {category}
      </button>
    {/each}
  </aside>

  <main class="grid flex-1 grid-cols-[repeat(auto-fill,minmax(160px,1fr))] content-start gap-4 overflow-y-auto p-4">
    {#each visibleItems as item (item.menu_item_id)}
      <button type="button" class="btn flex aspect-square flex-col items-center justify-center gap-1 font-medium">
        <span>{item.menu_item_name}</span>
        <span class="font-normal text-muted">${item.price.toFixed(2)}</span>
      </button>
    {/each}
  </main>
</div>
