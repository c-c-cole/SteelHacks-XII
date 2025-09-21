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
    const [serviceData, setServiceData] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/hospitals")
            .then((res) => res.json())
            .then((data) => {
                //console.log(data);
                setHospitals(data);
            })
            .catch(console.error);
    }, []);

    useEffect(() => {
        if (selectedHospital?.id) {
            fetch(`http://127.0.0.1:5000/service/${selectedHospital.id}`)
                .then(res => res.json())
                .then(data => {
                    setServiceData(data);
                })
                .catch(console.error);
        }
    }, [selectedHospital]);


    return (
        <LoadScript googleMapsApiKey={apiKey}
        language="en">
            <GoogleMap
                mapContainerStyle={containerStyle}
                center={center}
                zoom = {12}>
                {hospitals.map(([id, lat, lng, facility, address],index) => (
                <Marker 
                key = {index} 
                position={{ lat: lat, lng: lng}}
                onClick= {() => {
                    setSelectedHospital({id, lat, lng, facility, address, index})
                    if (onSelectHospital) {
                        onSelectHospital({id, lat, lng, facility, address, index});
                    }
                }}
                />
            ))}

            {selectedHospital && (
                <InfoWindow
                    position={{ lat: selectedHospital.lat, lng: selectedHospital.lng}}
                    onCloseClick= {() => {
                        setSelectedHospital(null);
                        setServiceData(null);
                    }}
                >
                    <div>
                        <h2>{selectedHospital.facility}</h2>
                        <p><strong></strong>{selectedHospital.address}</p>
                        {serviceData ? (
                            <>
                                <ul>
                                    <li>
                                        <p><strong>Nearest bus distance: </strong> {serviceData.nearestBusStopDist} mi</p>
                                    </li>
                                    <li>
                                        <p><strong>Median neighborhood income </strong> {serviceData.median_income} mi</p>
                                    </li>
                                </ul>


                                <p><strong>Accessibility:</strong> {(serviceData.A *10).toFixed(1)}/10</p>
                                <p><strong>Criticality:</strong> {(serviceData.C*10).toFixed(1)}/10</p>
                                <p><strong>Service Score:</strong> {(serviceData.G*10).toFixed(1)}/10</p>
                            </>
                        ) : (
                            <p>loading</p>
                        )}
                    </div>
                </InfoWindow>
            )}
            </GoogleMap>
        </LoadScript>
    );
};


export default Gmap;