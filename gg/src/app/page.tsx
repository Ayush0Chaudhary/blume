"use client";

import { Input } from "@/components/form";
import { _CLICKED_LOCATION, _MAP_PROPS } from "@/types";
import genereateDistanceMatrix from "@/utils/generateDistanceMatrix";
import { FormEvent, useState } from "react";

const mapUrl = process.env.NEXT_PUBLIC_MAPS_URL;



export default function Home() {
  const [warehouse, setWarehouse] = useState<number>(0);
  const [stores, setStores] = useState<number>(0);
  const [demand, setDemand] = useState<number>(0);
  // const [store_map_warehouse, setStoreMapWarehouse] = useState([["0", "0"]]);
  // const [vehicle_map_warehouse, setVehicleMapWarehouse] = useState([
  //   ["0", "0"],
  // ]);
  // const [demand_map, setDemandMap] = useState([["0", "0"]]);
  const [distanceMatrix, setDistanceMatrix] = useState<number[][]>([[]]);
  const [totalClicks, setTotalClicks] = useState<number>(0);
  const [clickedLocations, setClickedLocations] = useState<_CLICKED_LOCATION[]>(
    []
  );

  // Clicking mechanism
  const handleMapClick = (event: React.MouseEvent<HTMLImageElement>) => {
    const boundingBox = event.currentTarget.getBoundingClientRect();
    const clickedX = event.clientX - boundingBox.left;
    const clickedY = event.clientY - boundingBox.top;
    setTotalClicks((prevClicks) => prevClicks + 1);
    setDistanceMatrix(genereateDistanceMatrix(clickedLocations));

    setClickedLocations((prevLocations) => [
      ...prevLocations,
      { x: clickedX, y: clickedY },
    ]);
  };

  
  
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    let store_map_warehouse = [];
    let vehicle_map_warehouse = [];
    let demand:any[] = [];  
    const formData = new FormData(event.currentTarget);
    for (const entry of formData.entries()) {
      if (entry[0].includes("store_map_warehouse")) {
        const storeMap = entry[1].toString().split(",");
        store_map_warehouse.push(storeMap);
      } else if (entry[0].includes("vehicle_map_warehouse")) {
        const vehicleMap = entry[1].toString().split(",");
        vehicle_map_warehouse.push(vehicleMap);
      } else if (entry[0].includes("demand_map")) {
        const demandMap = entry[1].toString().split(",");
        demand.push(demandMap);
        console.log("Samosa", demand);
      }
    }

    // setStoreMapWarehouse(store_map_warehouse);
    // setVehicleMapWarehouse(vehicle_map_warehouse);
    // setDemandMap(demand_map);
    

      const data = {
        warehouse: warehouse,
        stores: stores,
        store_map: store_map_warehouse,
        vehicles_per_warehouse: vehicle_map_warehouse,
        Demand: demand,
        distanceMatrix: distanceMatrix,
      };

      const response = await fetch("http://127.0.0.1:5000/optimize", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
          "Access-Control-Allow-Origin": "*",
        },
      });
      console.log(await response.json());
    }

  // validation funtion
  function validate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    for (const entry of formData.entries()) {
      if (entry[0] === "warehouse") {
        setWarehouse(Number(entry[1]));
      } else if (entry[0] === "stores") {
        setStores(Number(entry[1]));
      } else if (entry[0] === "demand") {
        setDemand(Number(entry[1]));
      }
      console.log(warehouse, stores, demand);
    }
  }

  console.log(clickedLocations)

  return (
    <main className="flex min-h-screen flex-col justify-between p-24">
      <form onSubmit={onSubmit} onChange={validate}>
        <div className="flex flex-row gap-20">
          <Input
            name={"warehouse"}
            placeholder={"No. of warehouse"}
            type={"number"}
            label={"Warehouse"}
            isRequired={true}
            errorMessage={""}
          />
          <Input
            name={"stores"}
            placeholder={"No. of stores"}
            type={"number"}
            label={"Stores"}
            errorMessage={""}
            isRequired={true}
          />
          <Input
            name={"demand"}
            placeholder={"No. of demands"}
            type={"number"}
            label={"Demands"}
            errorMessage={""}
          />
        </div>
        {warehouse > 0 && stores > 0 && (
          <h1 className="text-xl ml-2 mb-5 text-red-400">
            Valid store number are from {warehouse + 1} to {warehouse + stores}
          </h1>
        )}
        {warehouse > 0 ? renderWarehouseInputs(warehouse) : ""}
        {demand > 0 ? renderDemandInputs(demand) : ""}
        <button
          className="text-2xl rounded-full bg-white text-black px-5 py-2"
          type="submit"
        >
          Submit
        </button>
      </form>
      
      <div className="relative my-10" style={{ width: 900 }}>
      <img
        src={mapUrl}
        alt="Static Map"
        style={{ width: "100%", height: "100%" }}
        onClick={totalClicks < warehouse + stores ? handleMapClick : () => {}}
        draggable={false}
      />
      {clickedLocations.map((location, index) => (
        <div
          key={index}
          id={`point${index}`}
          style={{
            position: "absolute",
            top: `${location.y}px`,
            left: `${location.x}px`,
            backgroundColor: totalClicks == 1 ? "red" : "blue",
            width: "15px",
            height: "15px",
            borderRadius: "50%",
          }}
        />
      ))}
    </div>
    </main>
  );
}


const renderWarehouseInputs = (n: number) => {
  const inputs = [];
  for (let i = 0; i < n; i++) {
    inputs.push(
      <div className="flex flex-row gap-10" key={i}>
        <Input
          name={`store_map_warehouse_${i + 1}`}
          placeholder={`comma separated store number`}
          type={"text"}
          label={`Stores for warehouse ${i + 1}`}
          errorMessage={""}
          isRequired={true}
        />
        <Input
          name={`vehicle_map_warehouse${i + 1}`}
          placeholder={`electric,truck`}
          type={"text"}
          label={`Vehicles for warehouse ${i + 1}`}
          errorMessage={""}
          isRequired={true}
        />
      </div>
    );
  }
  return inputs;
};
const renderDemandInputs = (n: number) => {
  const demandInputs = [];
  for (let i = 0; i < n; i++) {
    demandInputs.push(
      <div className="flex flex-row gap-10" key={i}>
        <Input
          name={`demand_map${i + 1}`}
          placeholder={`store,wgt,volume,drop_start,drop_end`}
          type={"text"}
          label={`Demand ${i + 1}`}
          errorMessage={""}
          isRequired={true}
        />
      </div>
    );
  }
  return demandInputs;
};