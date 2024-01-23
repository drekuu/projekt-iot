<script>
	import { onMount } from "svelte";

    let courses = [];
    let stops = [];
    let newStopName = "";
    const courseForm = {
        course_name: '',
        stops: ''
    }
    const baseUrl = "http://localhost:5173/api";
    let coursesUrl = "http://localhost:5173/api/courses";
    let stopsUrl = "http://localhost:5173/api/stops"
    onMount(async ()=>{
        courses = await getRoutes();
        stops = await getStops();
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

    async function getStops(){
        try{
            const response = await fetch(stopsUrl);
            const data = await response.json();
            const result = Object.keys(data).map(key => {
                return {
                    stop_id: key,
                    stop_name: data[key]
                }
            })
            return result;
        }catch(err){
            console.log(err);
        }
    }

 

    async function addStop(){

        if(newStopName === "") return;
        try{
            const url = `/addstop/${newStopName}`
            const response = await fetch(baseUrl + url, {
                method: "POST", 
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            if(response.ok){
                console.log("Form data sent successfully");
            }else{
                console.error("error sending form data", response.status);
            }
        }catch(e){
            console.log(e);
        }
        newStopName = '';
    }

    async function addCourse(){
        const stopsString = courseForm.stops;
        const courseName = courseForm.course_name.replace(/\s/g, '');
        const isValidInput = /^(\d+,)*\d*$/.test(stopsString);
        if(!isValidInput) return;
        if(courseName === "") return;
        if(stopsString === "") return;

        const stopsArray = stopsString.split(',').map(id => parseInt(id.trim(), 10));

        try{
            let url = `/addcourse/${courseName}?stops=`
            for(stop in stopsArray){
                url += `${stop},`;
            }
            url = url.slice(0, -1);
            const response = await fetch(baseUrl + url, {
                method: "POST", 
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            if(response.ok){
                console.log("Form data sent successfully");
            }else{
                console.error("error sending form data", response.status);
            }
        }catch(e){
            console.log(e);
        }
        
        courseForm.course_name = '';
        courseForm.stops = '';

    }


</script>


<div class=" p-3 flex flex-col justify-center items-center gap-8">

    <div class="flex flex-col justify-center items-center gap-8 p-3">
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

    <hr class=" border-[0.25px] border-black w-screen">

    <div>
        <h1 class=" text-xl"><strong>Available Stops</strong></h1>
        <div>
            {#each stops as stop}
                <div class=" flex flex-row gap-2">
                    <h2><strong>{stop.stop_id}</strong></h2>
                    <h2>{stop.stop_name}</h2>
                </div>
            {/each}
        </div>
    </div>

    <hr class=" border-[0.25px] border-black w-screen">
    
    <div class=" justify-center items-center flex flex-col gap-2">
        <h1 class=" text-xl"><strong>Add New Stop</strong></h1>
        <form on:submit|preventDefault={addStop} class=" flex flex-col justify-center items-center">
            <input class=" border-black border-2 p-2" type="text" placeholder="New Stop Name" id="stopName" name="stopName" bind:value={newStopName}>
            <label for="stopName" class=" hidden">Stop Name</label>
            <button type="submit">
                <i class="fa-solid fa-circle-plus text-4xl"></i>
            </button>
        </form>
        
    </div>

    <div class=" justify-center items-center flex flex-col gap-2">
        <h1 class=" text-xl"><strong>Add New Course</strong></h1>
        <form on:submit|preventDefault={addCourse} class=" flex flex-col justify-center items-center">
            <div class="flex flex-row">
                <input class=" border-black border-2 p-2" type="text" placeholder="New Course Name" id="courseName" name="courseName" bind:value={courseForm.course_name}>
                <label for="courseName" class=" hidden">Course Name</label>
                <input class=" border-black border-2 p-2" type="text" placeholder="Stops Ids: 1,2,3..." id="stops" name="stops" bind:value={courseForm.stops}>
                <label for="stops" class=" hidden">Stops</label>
            </div>
            <button type="submit">
                <i class="fa-solid fa-circle-plus text-4xl"></i>
            </button>
        </form>
       
    </div>

</div>