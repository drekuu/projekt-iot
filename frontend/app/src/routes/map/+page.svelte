<script>
	import { onDestroy, onMount } from "svelte";

    let buses = [];
    let courses = {};
    let refreshTime = 5;

    let busesUrl = "http://localhost:5173/api/buses";
    let coursesUrl = "http://localhost:5173/api/courses";

    onMount(async ()=>{
        courses = await getCourses();
        buses = await getBuses();
        startCountdown();
    });

    onDestroy(() => clearInterval(startCountdown));

    async function getBuses(){
        try{
            const response = await fetch(busesUrl);
            const data = await response.json();
            const result = Object.keys(data).map(key => {
                const entry = data[key];
                return {
                    number: key,
                    course_name: entry.course_name,
                    stop_number: entry.stop_number,
                    direction: entry.direction,
                }
            })
            return result;
        }catch(err){
            console.log(err);
        }
}

    async function getCourses(){
        try{
            const response = await fetch(coursesUrl);
            const data = await response.json();
            return data;
        }catch(err){
            console.log(err);
        }
    } 

    let countdown = refreshTime;
    const startCountdown = () => {
        setInterval(() => {
            countdown = (countdown - 1 + refreshTime) % refreshTime;
        }, 1000);
    };

    $: minutes = Math.floor(countdown / 60);
    $: seconds = countdown % 60;

    $: if(countdown === 0){
        getBuses().then((data) => {
            buses = data;
        }).catch((err) => {
            console.log(err);
        });
    }

    function refresh(){
        countdown = refreshTime;
    }
    

</script>



<div class=" flex flex-col items-start justify-start gap-10 h-screen p-10">

    <div class=" flex flex-row gap-2 items-center justify-center w-full">
        <h1><strong>Wait</strong></h1>
        <h1><strong>{`${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`}</strong></h1>
        <h1><strong>for the update or</strong></h1>
        <button on:click={refresh} class="bg-slate-300 rounded-lg p-1 text-white"><strong>refresh</strong></button>
    </div>

{#each buses as bus}
    {#if Object.keys(bus).length !== 0}
        <div class=" flex flex-row gap-2 items-center">
            <i class="fa-solid fa-bus text-4xl"></i>
            <div class=" flex flex-col ">
                <h1 class=" text-2xl"><strong>{"Bus nr. " + bus.number}</strong></h1>
                <h1  class=" text-2xl">{bus.course_name}</h1>
            </div>
            <div class=" ml-12 flex flex-row gap-28">
                {#if bus.course_name}
                    {#each courses[bus.course_name] as stop, i}
                        <div class=" flex flex-col justify-center items-center">
                            <i class="fa-solid fa-van-shuttle {bus.stop_number === i + 1 ? "text-green-600" : "text-transparent"} {bus.direction === "right" ? "" : "  scale-x-[-1]"} "></i>
                            <h1>{stop}</h1>
                        </div>
                    {/each} 
                {/if}
            </div>
        </div>
            
    {/if}
{/each}

</div>