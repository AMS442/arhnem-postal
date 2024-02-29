import django_filters
from dateutil.parser import parse
from django.db.models import Q
from django.shortcuts import render

from postcards.models import Collection, Location, Object, Person, Postmark


def get_names(field_prefix):
    """Get names from the Object model for a given field prefix (sender_name or addressee_name)."""
    return (
        Object.objects.exclude(
            **{f"{field_prefix}__first_name": "NA", f"{field_prefix}__last_name": "NA"}
        )
        .order_by(f"{field_prefix}__first_name", f"{field_prefix}__last_name")
        .values_list(f"{field_prefix}__first_name", f"{field_prefix}__last_name")
    )


def combine_all_names():
    """Combine all possible names from the Object senders and addressees for the dropdown."""
    all_names = list(get_names("sender_name")) + list(get_names("addressee_name"))
    all_names = [" ".join(map(str, name)) for name in all_names]
    all_names = [
        name for i, name in enumerate(all_names) if all_names.index(name) == i
    ]  # Only add names that are not already in the list
    all_names = [(name, name) for name in all_names]

    return all_names


class TownCityFilter(django_filters.ModelChoiceFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget.attrs.update(
            {"class": "form-control"}
        )  # Add Bootstrap form-control class
        self.field.queryset = Location.objects.values_list(
            "town_city", flat=True
        ).distinct()


class ProvinceStateFilter(django_filters.ModelChoiceFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget.attrs.update(
            {"class": "form-control"}
        )  # Add Bootstrap form-control class
        self.field.queryset = Location.objects.values_list(
            "province_state", flat=True
        ).distinct()


class ObjectFilter(django_filters.FilterSet):
    class Meta:
        model = Object
        fields = [
            "query",
            "correspondence",
            "date",
            "collection",
            "town_city",
            "province_state",
            "postmark",
        ]

    correspondence = django_filters.ChoiceFilter(
        choices=combine_all_names(),
        method="filter_query",
        label="Writer",
        empty_label="Select a writer",
    )
    date = django_filters.CharFilter(
        field_name="date_of_correspondence",
        lookup_expr="icontains",
        label="Date of correspondence",
    )
    collection = django_filters.ModelChoiceFilter(
        field_name="collection",
        queryset=Collection.objects.all(),
        to_field_name="name",
    )
    town_city = TownCityFilter(
        field_name="town_city",
        queryset=Location.objects.all(),
        label="Town/City",
    )
    province_state = ProvinceStateFilter(
        field_name="province_state",
        queryset=Location.objects.all(),
        label="Province/State",
    )
    postmark = django_filters.CharFilter(method="filter_by_postmark")
    query = django_filters.CharFilter(
        method="filter_query",
        label="Keyword search",
    )

    def filter_by_postmark(self, queryset, name, value):
        if value:
            # Check if ', dated ' is in the value string
            if ", dated " in value:
                # Split the value into location name and date
                location_name, date = value.split(", dated ", 1)
            else:
                # Set location_name to value and date to "unknown date"
                location_name, date = value, "unknown date"
            # Remove the "Postmarked at " prefix from the location name
            location_name = location_name.replace("Postmarked at ", "")
            # Check if the location name contains a comma
            if ", " in location_name:
                # Split the location name into town_city and country
                town_city, country = location_name.split(", ", 1)
            else:
                # Set town_city to location_name and country to an empty string
                town_city, country = location_name, ""
            # Create the query for town_city
            queries = Q(postmark__location__town_city__icontains=town_city)
            # If country is not an empty string, add a country query
            if country:
                queries &= Q(postmark__location__country__icontains=country)
            # If the date is not "unknown date", parse it and add a date query
            if date != "unknown date":
                date = parse(date).date()
                queries &= Q(postmark__date=date)
            # Filter the queryset
            return queryset.filter(queries)
        return queryset

    def filter_by_date(self, queryset, value):
        words = value.split(" ")
        queries = Q()
        for word in words:
            queries |= Q(date_of_correspondence__icontains=word)
        return queryset.filter(queries)

    def filter_by_name(self, queryset, value):
        first_name, last_name = value.split(" ", 1)
        queries = Q(
            sender_name__first_name=first_name, sender_name__last_name=last_name
        ) | Q(
            addressee_name__first_name=first_name, addressee_name__last_name=last_name
        )
        return queryset.filter(queries)

    def filter_by_city(self, queryset, value):
        print(f"Filtering by city: {value}")
        words = value.split(" ")
        queries = Q()
        for word in words:
            queries |= Q(location__town_city__icontains=word)
        print(f"Queries: {queries}")
        print(f"Queryset before filtering: {queryset}")
        queryset = queryset.filter(queries)
        print(f"Queryset after filtering: {queryset}")
        return queryset

    def filter_by_state(self, queryset, value):
        print(f"Filtering by state: {value}")
        words = value.split(" ")
        queries = Q()
        for word in words:
            queries |= Q(location__province_state__icontains=word)
        print(f"Queries: {queries}")
        print(f"Queryset before filtering: {queryset}")
        queryset = queryset.filter(queries)
        print(f"Queryset after filtering: {queryset}")
        return queryset

    def filter_by_collection(self, queryset, value):
        words = value.split(" ")
        queries = Q()
        for word in words:
            queries |= Q(collection__name__icontains=word)
        return queryset.filter(queries)

    def filter_by_public_notes(self, queryset, value):
        words = value.split(" ")
        queries = Q()
        for word in words:
            queries |= Q(public_notes__icontains=word)

    def filter_query(self, queryset, name, value):
        if name == "postmark":
            return self.filter_by_postmark(queryset, name, value)
        elif name == "date":
            return self.filter_by_date(queryset, value)
        elif name in [
            "correspondence",
        ]:
            return self.filter_by_name(queryset, value)
        elif name in ["town_city"]:
            return self.filter_by_city(queryset, value)
        elif name in ["province_state"]:
            return self.filter_by_state(queryset, value)
        elif name == "collection":
            return self.filter_by_collection(queryset, value)
        elif name == "keywords":
            return self.filter_by_public_notes(queryset, value)
        else:
            return queryset
