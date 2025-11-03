import random
from datetime import datetime, timedelta

def dummyDATA():
   
    employee_names = [
        "Ali Khan", "Sarah Malik", "Usman Raza", "David Smith", "Hamza Iqbal",
        "Adeel Ahmed", "Maria Ali", "John Evans", "Bilal Khan", "Asif Nawaz",
        "Omar Farooq", "Ahmed Saleem", "Khalid Hussain", "Sophie Turner", "Imran Qureshi",
        "Zainab Shah", "Tariq Mahmood", "Nadia Hussain", "James Brown", "Hassan Rafiq",
        "Emma Wilson", "Liam Johnson", "Olivia Taylor", "Noah Anderson", "Chloe Williams",
        "Ayaan Siddiqui", "Fatima Zahra", "Leo Carter", "Mia Thompson", "Ethan White",
        "Isabella Green", "Alexander Hall", "Amelia Baker", "Daniel Young", "Layla Scott"
    ]

    client_names = [
        "Tesco Express", "Barclays Bank", "Hilton Hotel", "Amazon Warehouse",
        "NHS Clinic", "Sainsburys", "Primark", "BP Petrol Station", "Lidl Supermarket",
        "Construction Site", "Morrisons", "Boots Pharmacy", "Asda", "Argos",
        "IKEA", "KFC", "McDonalds", "Costa Coffee", "Greggs", "Co-op Food",
        "Waitrose", "Marks & Spencer", "Starbucks", "Shell Petrol", "Holiday Inn",
        "Premier Inn", "Apple Store", "Currys", "JD Sports", "B&Q", "Tesco Metro",
        "Next Retail", "Pizza Hut", "Nando's", "Subway", "O2 Store", "Vodafone Store"
    ]

    site_locations = [
        "14 High Street, London", "22 Oxford Road, Slough", "1 Park Lane, London",
        "45 Industrial Estate, Croydon", "88 Green Street, Birmingham",
        "32 Queens Road, London", "10 Market Square, Reading",
        "2 A406 North Circular, London", "71 Main Street, Luton",
        "18 Docklands Road, London", "5 City Centre, Manchester",
        "9 Broad Street, Nottingham", "12 Albert Road, Leeds",
        "55 Riverside, Glasgow", "17 Central Avenue, Cardiff",
        "66 South Road, Bristol", "42 Meadow Lane, Leicester",
        "21 Market Street, Liverpool", "73 Park Avenue, Sheffield", "89 Oxford Street, London",
        "101 Victoria Street, London", "77 King Street, Manchester", "33 Queensway, Birmingham",
        "50 Canary Wharf, London", "8 Regent Street, London", "60 Oxford Circus, London",
        "44 Piccadilly, London", "12 Shad Thames, London", "27 Borough High Street, London"
    ]

    shift_schedules = []
    for i in range(400):
        start_time = datetime.now() - timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))
        duration_hours = random.choice([6, 8, 10, 12])
        end_time = start_time + timedelta(hours=duration_hours)
        shift_id = f"SHIFT-{i+1:03d}"
        supervisor = random.choice(employee_names)
        
        shift_schedules.append({
            "shift_id": shift_id,
            "shift_start": start_time.strftime("%Y-%m-%d %H:%M"),
            "shift_end": end_time.strftime("%Y-%m-%d %H:%M"),
            "duration_hours": duration_hours,
            "supervisor": supervisor
        })

    incident_reports = [
        "No incidents reported. Routine patrol completed.",
        "Suspicious person observed near entrance; reported to supervisor.",
        "Fire alarm triggered accidentally; false alarm confirmed.",
        "Minor theft detected; police informed.",
        "Unauthorized vehicle attempted access; stopped by guard.",
        "Customer lost item; returned after verification.",
        "Power outage; backup generator activated successfully.",
        "Dispute between visitors resolved peacefully.",
        "Suspicious bag checked; no threat found.",
        "Intruder fled after alarm triggered.",
        "Glass door damage due to wind; maintenance notified.",
        "Alarm malfunction; engineer called for service.",
        "Employee locked out; entry authorized by manager.",
        "Vandalism attempt recorded on CCTV; report filed.",
        "Parking lot altercation handled by on-site staff.",
        "Water leak detected in basement; maintenance alerted.",
        "Door left open by mistake; secured immediately.",
        "Visitor denied entry without proper ID; incident logged.",
        "Security camera briefly offline; system rebooted.",
        "Lost and found item returned to rightful owner."
    ]

    statuses = ["Secure", "Under Review", "High Risk", "Pending Maintenance", "Investigation Ongoing", "Resolved", "Monitoring", "Critical", "Completed"]

    response_times = ["2 minutes", "3 minutes", "4 minutes", "5 minutes", "6 minutes",
                      "7 minutes", "8 minutes", "9 minutes", "10 minutes", "N/A", "12 minutes", "15 minutes", "20 minutes"]

    business_list = []
    
    for i in range(200):
        employee = random.choice(employee_names)
        client = random.choice(client_names)
        site_location = random.choice(site_locations)
        shift_schedule = random.choice(shift_schedules)
        incident_report = random.choice(incident_reports)
        status = random.choice(statuses)
        response_time = random.choice(response_times)
        rating = random.randint(1, 5)

        reviews = []
        for _ in range(random.randint(2, 5)):
            controller = random.choice(employee_names)
            review_text = random.choice(incident_reports)
            reviews.append({
                "controller": controller,
                "review": review_text,
                "rating": rating,
            })

        business = {
            "employee_name": employee,
            "client_name": client,
            "site_location": site_location,
            "shift_schedule": shift_schedule,
            "incident_report": incident_report,
            "status": status,
            "response_time": response_time,
            "rating": rating,
            "reviews": reviews
        }

        business_list.append(business)

    return business_list
