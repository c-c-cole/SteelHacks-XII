import React from "react";
import { GoogleMap, LoadScript } from '@react-google-maps/api';

const containerStyle = {
    width: '100%',
    height: '400px',
};

const center = {
    lat: 40.4387,
    lng: -79.9972,
};

const Gmap = () => {
    const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY


    return (
        <LoadScript googleMapsApiKey={apiKey}
        language="en">
            <GoogleMap
                mapContainerStyle={containerStyle}
                center={center}
                zoom = {15}
> 
            </GoogleMap>
        </LoadScript>
    );
};

export default Gmap;