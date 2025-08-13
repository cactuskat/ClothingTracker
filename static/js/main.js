const debug = 1;

// === Classes ===
class Clothing {
    constructor({id=null,name=null,type=null,weather=null,path=null} = {}){
    this.id = id;
    this.name = null;
    this.type = type;
    this.weather = weather;
    this.path = path;}
}
class Outfit {
    constructor({top=null, bottom=null, accessory=null} = {}){
    this.top = top; 
    this.bottom = bottom;
    this.accessory = accessory;
    }
}

// === Global Variables ===
let isAccessoryActive;

// === DOM Functions ===  
document.getElementById("outfitCreatorForm").addEventListener("submit",async(event) => {
    event.preventDefault();
    await updateMannequin();
})
document.getElementById("accessoryBtn").accessKeyLabel("click", function () {

})


// === Weather API ===
/*
Purpose: Fetches weather condition based on console location or input zipcode
Input: NONE
Return: hot(>=75), mid(74-60), cold(<= 60)
*/
async function fetchWeather() {
    if (debug) {return "hot";}
    let query;
    try {
        // Determine location
        const zipcodeTextbox = document.getElementById("zipcodeTextbox");
        if(!zipcodeTextbox) {throw new Error("fetchWeather Error: no zipcode textbox");}

        if (zipcodeTextbox.value.trim().length > 0)
        {
        const zipcode = zipcodeTextbox.value.trim();
        query = `/weather/get/today?zipcode=${zipcode}`;
        if (debug) {console.log(`Zipcode:${zipcode})`);} 
        } else {
        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve,reject);});
        const lon = position.coords.longitude;
        const lat = position.coords.latitude;
        query = `/weather/get/today?lat=${lat}&lon=${lon}`;
        if (debug) {console.log(`Coords:(${lat},${lon})`);}
        }

        // Fetch location weather data
        const response = await fetch(query);
        if (!response.ok) { throw new Error(`Fetch error: ${response.status}`);}

        const result = await response.json();
        if (debug) {console.log('fetchWeather JSON data :',result);}

        // Return weather
        const temp = result.temp;
        if (debug) {console.log("Temp:",temp)}
        if (temp >= 75){
        return "hot";
        } else if (temp <= 60){
        return "cold";
        } else {
        return "mid";
        }
    } catch (error) {
        console.error(error.message);
        return null;
    }
}
  
// === Outfit Handling ===
/*
Purpose: Creates an outfit according to the weather & accessory choice
Input: NONE
Return: VOID
*/
async function createOutfit(){
    const outfit = new Outfit();
    isAccessoryActive = document.getElementById("accessoryBtn").checked;
    weather = await fetchWeather();

    for (const clothingType of Object.keys(outfit)) {
    if (!isAccessoryActive && clothingType === "accessory") {continue;} 
    const clothingWeather = (isAccessoryActive && clothingType === "accessory") ? "all" : weather;
    const response = await fetchClothing(clothingType,clothingWeather);
    if (!response){
        console.log(`No data returned from fetchClothing(${clothingType},${clothingWeather})`);
    } else if (response.error){
        console.log("Error from backend:",response.error);
    }

    outfit[clothingType] = new Clothing({
    id:response.id,
    name:response.name,
    type:clothingType,
    weather:clothingWeather,
    path:response.path});
    }

    if (debug) console.log("Created outfit:",outfit);
    return outfit;
}

/*
Purpose: Fetches a clothing from closet_list.db
Input: clothingType (clothing object type), Weather(temp of user)
Return: clothing object data
*/
async function fetchClothing(clothingType,weather){
    if (debug) {console.log(`fetchClothing with ${clothingType} & ${weather}`)}
    try {
    const response = await fetch(`/clothing/search?type=${encodeURIComponent(clothingType)}&weather=${encodeURIComponent(weather)}`);
    if (!response.ok) { throw new Error(`Fetch error: ${response.status}`);}
    const result = await response.json();
    if (debug) {console.log('fetchClothing JSON data:',result);}
    return result;
    } catch (error) {
    console.error(error.message);
    return null;
    }
}

/*
Purpose: Displays generated outfit
Input: NONE
Return: VOID
*/
async function updateMannequin(){   
    //Generates an outfit
    const mannequinOutfit = await createOutfit();
    if (debug) console.log("Dressed mannequin:",mannequinOutfit);

    // Update Image of generated outfit
    for (const clothingType of Object.keys(mannequinOutfit)){ 
    const element = document.getElementById(clothingType);
    if (!element) {continue;}
    
    const item = mannequinOutfit[clothingType];

    if (item && item.path) {
        element.src = "/static/" +  item.path;
        element.alt = item.name;
        if (debug) {console.log("Image Mannequinn:",clothingType);}
        continue;
    }
    // if no image or item if found, a placeholder will be placed
    element.src = "/static/imgs/Placeholders/blank.png";
    element.alt = "blank";
    }
}





