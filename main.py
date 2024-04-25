from fastapi import FastAPI, Query
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base
import csv
from datetime import datetime

# Define the SQLite database connection
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our SQLAlchemy models
Base = declarative_base()


# Define a model for our database table
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, index=True)
    data_year = Column(Integer, index=True)
    ori = Column(String, index=True)
    pug_agency_name = Column(String, index=True)
    pub_agency_unit = Column(String, index=True)
    agency_type_name = Column(String, index=True)
    state_abbr = Column(String, index=True)
    state_name = Column(String, index=True)
    division_name = Column(String, index=True)
    region_name = Column(String, index=True)
    population_group_code = Column(Integer, index=True)
    population_group_description = Column(String, index=True)
    incident_date = Column(Date, index=True)
    adult_victim_count = Column(Integer)
    juvenile_victim_count = Column(Integer)
    total_offender_count = Column(Integer)
    adult_offender_count = Column(Integer)
    juvenile_offender_count = Column(Integer)
    offender_race = Column(String)
    offender_ethnicity = Column(String)
    victim_count = Column(Integer)
    offense_name = Column(String)
    total_individual_victims = Column(Integer)
    location_name = Column(String)
    bias_desc = Column(String)
    victim_types = Column(String)
    multiple_offense = Column(String)
    multiple_bias = Column(String)


# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()


# Function to read data from CSV file and add it to the database
def load_data_from_csv():
    with open('cleaned_hate_crime.csv', 'r') as file:
        reader = csv.DictReader(file)
        incidents = []
        for row in reader:
            incident_date = datetime.strptime(row['incident_date'], '%Y-%m-%d').date()
            incidents.append(Incident(
                incident_id=row['incident_id'],
                data_year=row['data_year'],
                ori=row['ori'],
                pug_agency_name=row['pug_agency_name'],
                agency_type_name=row['agency_type_name'],
                state_abbr=row['state_abbr'],
                state_name=row['state_name'],
                division_name=row['division_name'],
                region_name=row['region_name'],
                population_group_code=row['population_group_code'],
                population_group_description=row['population_group_description'],
                incident_date=incident_date,
                total_offender_count=row['total_offender_count'],
                offender_race=row['offender_race'],
                victim_count=row['victim_count'],
                offense_name=row['offense_name'],
                total_individual_victims=row['total_individual_victims'],
                location_name=row['location_name'],
                bias_desc=row['bias_desc'],
                victim_types=row['victim_types'],
                multiple_offense=row['multiple_offense'],
                multiple_bias=row['multiple_bias']
            ))
    db = SessionLocal()
    db.add_all(incidents)
    db.commit()
    db.close()


# Load data from CSV into the database
load_data_from_csv()


# GET endpoint to fetch paginated incidents from the database with filtering options
@app.get("/incidents")
def get_incidents(
        data_year: int = None,
        state_name: str = None,
        location_name: str = None,
        offender_race: str = None,
        victim_types: str = None,
        bias_desc: str = None,
        public_agency_name: str = None,
        public_agency_unit: str = None,
        agency_type_name: str = None,
        state_abbr: str = None,
        division_name: str = None,
        region_name: str = None,
        population_group_code: int = None,
        population_group_description: str = None,
        incident_date: datetime = None,
        adult_victim_count: int = None,
        juvenile_victim_count: int = None,
        total_offender_count: int = None,
        adult_offender_count: int = None,
        juvenile_offender_count: int = None,
        victim_count: int = None,
        offense_name: str = None,
        total_individual_victims: int = None,
        multiple_offense: str = None,
        multiple_bias: str = None,
        incident_year: int = Query(None, ge=2000, le=2020),
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=100)
):
    db = SessionLocal()
    query = db.query(Incident)
    if data_year is not None:
        query = query.filter(Incident.data_year == data_year)
    if state_name is not None:
        query = query.filter(Incident.state_name.like(f"%{state_name}%"))
    if location_name is not None:
        query = query.filter(Incident.location_name.like(f"%{location_name}%"))
    if offender_race is not None:
        query = query.filter(Incident.offender_race.like(f"%{offender_race}%"))
    if victim_types is not None:
        query = query.filter(Incident.victim_types.like(f"%{victim_types}%"))
    if bias_desc is not None:
        query = query.filter(Incident.bias_desc.like(f"%{bias_desc}%"))
    if public_agency_name is not None:
        query = query.filter(Incident.pug_agency_name.like(f"%{public_agency_name}%"))
    if public_agency_unit is not None:
        query = query.filter(Incident.pub_agency_unit.like(f"%{public_agency_unit}%"))
    if agency_type_name is not None:
        query = query.filter(Incident.agency_type_name.like(f"%{agency_type_name}%"))
    if state_abbr is not None:
        query = query.filter(Incident.state_abbr.like(f"%{state_abbr}%"))
    if division_name is not None:
        query = query.filter(Incident.division_name.like(f"%{division_name}%"))
    if region_name is not None:
        query = query.filter(Incident.region_name.like(f"%{region_name}%"))
    if population_group_code is not None:
        query = query.filter(Incident.population_group_code == population_group_code)
    if population_group_description is not None:
        query = query.filter(Incident.population_group_description.like(f"%{population_group_description}%"))
    if incident_date is not None:
        query = query.filter(Incident.incident_date == incident_date)
    if adult_victim_count is not None:
        query = query.filter(Incident.adult_victim_count == adult_victim_count)
    if juvenile_victim_count is not None:
        query = query.filter(Incident.juvenile_victim_count == juvenile_victim_count)
    if total_offender_count is not None:
        query = query.filter(Incident.total_offender_count == total_offender_count)
    if adult_offender_count is not None:
        query = query.filter(Incident.adult_offender_count == adult_offender_count)
    if juvenile_offender_count is not None:
        query = query.filter(Incident.juvenile_offender_count == juvenile_offender_count)
    if victim_count is not None:
        query = query.filter(Incident.victim_count == victim_count)
    if offense_name is not None:
        query = query.filter(Incident.offense_name.like(f"%{offense_name}%"))
    if total_individual_victims is not None:
        query = query.filter(Incident.total_individual_victims == total_individual_victims)
    if multiple_offense is not None:
        query = query.filter(Incident.multiple_offense.like(f"%{multiple_offense}%"))
    if multiple_bias is not None:
        query = query.filter(Incident.multiple_bias.like(f"%{multiple_bias}%"))
    if incident_year is not None:
        query = query.filter(Incident.incident_date >= datetime(incident_year, 1, 1))
        query = query.filter(Incident.incident_date <= datetime(incident_year, 12, 31))
    incidents = query.offset(skip).limit(limit).all()
    db.close()
    return incidents