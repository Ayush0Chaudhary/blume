// #region Form Component

// InputProps
export type _INPUT_PROPS = {
  name: string;
  placeholder: string;
  type: string;
  isRequired?: boolean;
  label: string;
  errorMessage: string;
};

// FileInputProps
export type _FILE_INPUT_PROPS = {
  isRequired: boolean;
  label: string;
  accept?: string;
  errorMessage: string;
};

// CheckboxProps
export type _CHECKBOX_PROPS = {
  name: string;
  label: string;
  default_value?: boolean;
  isRequired?: boolean;
  value: string;
  errorMessage: string;
};

// SelectProps

// export type _SELECT_OPTION = {
//   value: string;
//   label: string;
// };

export type _SELECT_PROPS = {
  name: string;
  options: string[];
  isRequired?: boolean;
  label: string;
  errorMessage: string;
};



export type _FORM_PROPS = {
  warehouse:number;
  store_map_warehouse: Array<Array<number>>;
  vehicle_map_warehouse: Array<Array<number>>;
  demand_map: Array<Array<any>>;
  distance_matrix: Array<Array<number>>;
}
// #endregion Form Component

// #region Map Component

export type _MAP_PROPS = {
  warehouse:number;
  stores:number;
  apiKey:string;
  location: {lat:number,lng:number};
}

export type _CLICKED_LOCATION = {
  x:number;
  y:number;
}