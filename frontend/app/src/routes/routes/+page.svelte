<script>
	import { onMount } from "svelte";

    let courses = [];
    let coursesUrl = "http://localhost:5173/api/courses";
    onMount(async ()=>{
        courses = await getRoutes();
    });

    async function getRoutes(){
        try{
            const response = await fetch(coursesUrl);
            const data = await response.json();
            const result = Object.keys(data).map(key => {
                return {
                    course_name: key,
                    stops: data[key]
                }
            })
            return result;
        }catch(err){
            console.log(err);
        }
    }


</script>


<div class=" p-3 flex flex-col justify-center items-center gap-8">

    {#each courses as course}
    <div class=" flex flex-col">
        <div class=" flex flex-row gap-4 text-3xl bg-slate-300 p-2">
            <h3>{course.course_name}</h3>
        </div>
        {#each course.stops as stop, i}
            <div class=" flex flex-row gap-2">
                <p><strong>{i + 1}</strong></p>
                <p>{stop}</p>
            </div>
        {/each}
    </div>
    {/each}

</div>