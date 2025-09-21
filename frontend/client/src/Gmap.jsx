import React, { useEffect, useState } from "react";
import { GoogleMap, LoadScript, Marker, InfoWindow } from '@react-google-maps/api';


const containerStyle = {
    width: '100%',
    height: '400px',
};


const center = {
    lat: 40.4387,
    lng: -79.9972,
};


const Gmap = ({ onSelectHospital }) => {
    const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
    const [hospitals, setHospitals] = useState([]);
    const [selectedHospital, setSelectedHospital] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/hospitals")
            .then((res) => res.json())
            .then((data) => {
                console.log(data);
                setHospitals(data);
            })
            .catch(console.error);
    }, []);


    return (
        <LoadScript googleMapsApiKey={apiKey}
        language="en">
            <GoogleMap
                mapContainerStyle={containerStyle}
                center={center}
                zoom = {12}>
                {hospitals.map(([lat, lng, facility, address],index) => (
                <Marker 
                key = {index} 
                position={{ lat: lat, lng: lng}}
                onClick= {() => {
                    setSelectedHospital({ lat, lng, facility, address, index})
                    if (onSelectHospital) {
                        onSelectHospital({ lat, lng, facility, address, index});
                    }
                }}
                />
            ))}

            {selectedHospital && (
                <InfoWindow
                    position={{ lat: selectedHospital.lat, lng: selectedHospital.lng}}
                    onCloseClick= {() => setSelectedHospital(null)}
                >
                    <div>
                        <h2>{selectedHospital.facility}</h2>
                        <p><strong></strong>{selectedHospital.address}</p>
                        <h3><strong>Latitude: </strong> {selectedHospital.lat}</h3>
                        <h3><strong>Longitude: </strong> {selectedHospital.lng}</h3>
                    </div>
                </InfoWindow>
            )}
            </GoogleMap>
        </LoadScript>
    );
};


export default Gmap;