<script>
import { page } from '$app/stores';

</script>


<div class=" flex flex-row justify-center items-center p-5 gap-8 bg-slate-300 shadow-md h-24">
    <i class="fa-solid fa-bus text-2xl"></i>
    <a class:border-b-4={$page.url.href?.includes('/employees')} class=" border-white text-xl hover:text-white" href="/employees">
        Employees
    </a>
    <a class:border-b-4={$page.url.href?.includes('/map')} class=" border-white text-xl hover:text-white" href="/map">
        Map
    </a>
    <a class:border-b-4={$page.url.href?.includes('/routes')} class=" border-white text-xl hover:text-white" href="/routes">
        Routes
    </a>
</div>