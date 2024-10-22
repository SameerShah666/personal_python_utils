healthcaresystem = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthcareSystem {
    struct MedicalHistory {
        string bloodGroup;
        string[] allergies;
        string[] chronicDiseases;
        string[] currentMedications;
        string[] familyMedicalHistory;
        string lifestyleFactors;
        string[] knownConditions;
    }

    struct MedicalData {
        string[] previousDiagnostics;
        string[] injuries;
        string[] surgeries;
        string[] reports;
    }

    struct Patient {
        string name;
        uint age;
        MedicalHistory medicalHistory;
        MedicalData medicalData;
        bool exists;
    }

    mapping(address => Patient) private patients;
    mapping(address => bool) private doctors;

    event PatientAdded(address indexed patientAddress, string name);
    event PatientUpdated(address indexed patientAddress, string medicalHistorySummary);

    modifier onlyDoctor() {
        require(doctors[msg.sender], "Only doctors can perform this action");
        _;
    }

    modifier onlyPatient(address _patientAddress) {
        require(msg.sender == _patientAddress, "Not authorized");
        _;
    }

    // Function to add a doctor
    function addDoctor(address _doctorAddress) external {
        require(!doctors[_doctorAddress], "Doctor already exists");
        doctors[_doctorAddress] = true;
    }

    // Function to remove a doctor
    function removeDoctor(address _doctorAddress) external {
        require(doctors[_doctorAddress], "Doctor does not exist");
        doctors[_doctorAddress] = false;
    }

    // Function to add a patient
    function addPatient(
        address _patientAddress,
        string memory _name,
        uint _age
    ) external onlyDoctor {
        require(!patients[_patientAddress].exists, "Patient already exists");

        // Initialize basic patient details
        Patient storage patient = patients[_patientAddress];
        patient.name = _name;
        patient.age = _age;
        patient.exists = true;

        emit PatientAdded(_patientAddress, _name);
    }

    // Function to initialize medical history
    function initializeMedicalHistory(
        address _patientAddress,
        string memory _bloodGroup,
        string[] memory _allergies,
        string[] memory _chronicDiseases,
        string[] memory _currentMedications,
        string[] memory _familyMedicalHistory,
        string memory _lifestyleFactors,
        string[] memory _knownConditions
    ) external onlyDoctor {
        require(patients[_patientAddress].exists, "Patient does not exist");

        MedicalHistory storage medicalHistory = patients[_patientAddress].medicalHistory;
        medicalHistory.bloodGroup = _bloodGroup;
        medicalHistory.allergies = _allergies;
        medicalHistory.chronicDiseases = _chronicDiseases;
        medicalHistory.currentMedications = _currentMedications;
        medicalHistory.familyMedicalHistory = _familyMedicalHistory;
        medicalHistory.lifestyleFactors = _lifestyleFactors;
        medicalHistory.knownConditions = _knownConditions;
    }

    // Function to initialize medical data
    function initializeMedicalData(
        address _patientAddress,
        string[] memory _previousDiagnostics,
        string[] memory _injuries,
        string[] memory _surgeries,
        string[] memory _reports
    ) external onlyDoctor {
        require(patients[_patientAddress].exists, "Patient does not exist");

        MedicalData storage medicalData = patients[_patientAddress].medicalData;
        medicalData.previousDiagnostics = _previousDiagnostics;
        medicalData.injuries = _injuries;
        medicalData.surgeries = _surgeries;
        medicalData.reports = _reports;

        emit PatientUpdated(_patientAddress, "Medical data updated.");
    }

    // Function to update patient medical history
    function updatePatientMedicalHistory(
        address _patientAddress,
        string memory _bloodGroup,
        string[] memory _allergies,
        string[] memory _chronicDiseases,
        string[] memory _currentMedications,
        string[] memory _familyMedicalHistory,
        string memory _lifestyleFactors,
        string[] memory _knownConditions
    ) external onlyDoctor {
        require(patients[_patientAddress].exists, "Patient does not exist");

        MedicalHistory storage medicalHistory = patients[_patientAddress].medicalHistory;
        medicalHistory.bloodGroup = _bloodGroup;
        medicalHistory.allergies = _allergies;
        medicalHistory.chronicDiseases = _chronicDiseases;
        medicalHistory.currentMedications = _currentMedications;
        medicalHistory.familyMedicalHistory = _familyMedicalHistory;
        medicalHistory.lifestyleFactors = _lifestyleFactors;
        medicalHistory.knownConditions = _knownConditions;

        emit PatientUpdated(_patientAddress, "Medical history updated.");
    }

    // Split functions to return patient data in smaller parts
    function getPatientBasicInfo(address _patientAddress) external view returns (string memory name, uint age) {
        require(msg.sender == _patientAddress || doctors[msg.sender], "Not authorized to view this patient's data");
        Patient storage patient = patients[_patientAddress];

        require(patient.exists, "Patient does not exist");

        return (patient.name, patient.age);
    }

    function getMedicalHistory(address _patientAddress) external view returns (
        string memory bloodGroup,
        string[] memory allergies,
        string[] memory chronicDiseases,
        string[] memory currentMedications,
        string[] memory familyMedicalHistory,
        string memory lifestyleFactors,
        string[] memory knownConditions
    ) {
        require(msg.sender == _patientAddress || doctors[msg.sender], "Not authorized to view this patient's data");
        Patient storage patient = patients[_patientAddress];

        require(patient.exists, "Patient does not exist");

        MedicalHistory storage history = patient.medicalHistory;

        return (
            history.bloodGroup,
            history.allergies,
            history.chronicDiseases,
            history.currentMedications,
            history.familyMedicalHistory,
            history.lifestyleFactors,
            history.knownConditions
        );
    }

    function getMedicalData(address _patientAddress) external view returns (
        string[] memory previousDiagnostics,
        string[] memory injuries,
        string[] memory surgeries,
        string[] memory reports
    ) {
        require(msg.sender == _patientAddress || doctors[msg.sender], "Not authorized to view this patient's data");
        Patient storage patient = patients[_patientAddress];

        require(patient.exists, "Patient does not exist");

        MedicalData storage data = patient.medicalData;

        return (
            data.previousDiagnostics,
            data.injuries,
            data.surgeries,
            data.reports
        );
    }
}
'''