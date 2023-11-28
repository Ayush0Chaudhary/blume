import { _CLICKED_LOCATION } from "@/types";

export default function genereateDistanceMatrix(locations:_CLICKED_LOCATION[]){
   let distance_matrix = [];
    for (let i = 0; i < locations.length; i++) {
        let row = [];
        for (let j = 0; j < locations.length; j++) {
            row.push(calculateDistance(locations[i],locations[j]));
        }
        distance_matrix.push(row);
    }   
    return distance_matrix;
}

function calculateDistance(location1:_CLICKED_LOCATION,location2:_CLICKED_LOCATION) {
    return Math.sqrt(Math.pow(location1.x-location2.x,2)+Math.pow(location1.y-location2.y,2));
}