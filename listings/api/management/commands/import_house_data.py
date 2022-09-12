from django.core.management.base import BaseCommand, CommandError
from api.models import FleetDailyTrips
import csv
from datetime import datetime
import pandas as pd

class Command(BaseCommand):
    help = 'Imports data about houses'

    def add_arguments(self, parser):
        # TODO: Add any arguments here
        parser.add_argument('--file_path', type=str, help="complete file path to load data")

    def handle(self, *args, **options):
        # TODO: implement your import command
        df = pd.read_csv (options["file_path"])
        df2 = df.fillna("")
        daily_trips = []
        for index, row in df2.iterrows():
            daily_trip = FleetDailyTrips(
                date = datetime.strptime(row[0], "%d/%m/%y").date(),
                fare_total = row[1],
                trips = row[2],
                hours_online = row[3],
                total_km = row[4],
                rating = row[5],
                acceptance_rate_perc = row[6],
                driver_cancellation_rate = row[7],
                driver_id = row[8] if row[8] != "" else None,
                car_id = row[9] if row[9] != "" else None,
                cash_collected = row[10],
                toll = row[11],
                team_id = row[12] if row[12] != "" else None,
            )
            daily_trips.append(daily_trip)
        if daily_trips:
            FleetDailyTrips.objects.bulk_create(daily_trips)
        self.stdout.write("Import completed")