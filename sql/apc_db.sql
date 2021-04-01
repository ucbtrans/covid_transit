-- Table: public.actransit

-- DROP TABLE public.actransit;

CREATE TABLE public.actransit
(
    stop_id bigint NOT NULL,
    stop_name character varying(41) COLLATE pg_catalog."default",
    route bigint NOT NULL,
    trip character(4) COLLATE pg_catalog."default" NOT NULL,
    stop_seq_id integer NOT NULL,
    bus bigint NOT NULL,
    act_stop_time timestamp without time zone NOT NULL,
    direction character(1) COLLATE pg_catalog."default" NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    psgr_on integer NOT NULL,
    psgr_off integer NOT NULL,
    psgr_load integer NOT NULL,
    val_full integer NOT NULL,
    val_overcrowd integer NOT NULL,
    num_wc_recs integer NOT NULL,
    num_sp1_recs integer NOT NULL,
    num_sp2_recs integer NOT NULL,
    dwell_tot_mins double precision NOT NULL,
    cars integer NOT NULL
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.actransit
    OWNER to postgres;

COMMENT ON TABLE public.actransit
    IS 'AC Transit APC data.';

COMMENT ON COLUMN public.actransit.stop_id
    IS 'Unique stop ID';

COMMENT ON COLUMN public.actransit.stop_name
    IS 'Name of the stop';

COMMENT ON COLUMN public.actransit.route
    IS 'Route ID';

COMMENT ON COLUMN public.actransit.trip
    IS 'Scheduled trip start time (text: 4 characters)';

COMMENT ON COLUMN public.actransit.stop_seq_id
    IS 'Stop sequence number on route';

COMMENT ON COLUMN public.actransit.bus
    IS 'Vehicle ID';

COMMENT ON COLUMN public.actransit.act_stop_time
    IS 'Actual arrival time at the stop';

COMMENT ON COLUMN public.actransit.direction
    IS 'Direction code';

COMMENT ON COLUMN public.actransit.latitude
    IS 'Latitude of the stop (no correction)';

COMMENT ON COLUMN public.actransit.longitude
    IS 'Longitude of the stop (no correction)';

COMMENT ON COLUMN public.actransit.psgr_on
    IS 'Number of passengers boarding at stop';

COMMENT ON COLUMN public.actransit.psgr_off
    IS 'Number of passengers deboarding at stop';

COMMENT ON COLUMN public.actransit.psgr_load
    IS 'The total number of passengers on the bus at stop departure';

COMMENT ON COLUMN public.actransit.val_full
    IS 'Values of Full capacity for bus';

COMMENT ON COLUMN public.actransit.val_overcrowd
    IS 'Overcrowding values for bus';

COMMENT ON COLUMN public.actransit.num_wc_recs
    IS 'Number of wheelchair records at this stop';

COMMENT ON COLUMN public.actransit.num_sp1_recs
    IS 'Number of 1st bike rack records at this stop';

COMMENT ON COLUMN public.actransit.num_sp2_recs
    IS 'Number of 2nd bike rack records at this stop';



-- Table: public.tridelta

-- DROP TABLE public.tridelta;

CREATE TABLE public.tridelta
(
    stop_id bigint NOT NULL,
    stop_name character varying(64) COLLATE pg_catalog."default",
    route bigint NOT NULL,
    trip character(4) COLLATE pg_catalog."default" NOT NULL,
    stop_seq_id integer NOT NULL,
    bus bigint NOT NULL,
    act_stop_time timestamp without time zone NOT NULL,
    direction character(1) COLLATE pg_catalog."default" NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    psgr_on integer NOT NULL,
    psgr_off integer NOT NULL,
    psgr_load integer NOT NULL,
    val_full integer NOT NULL,
    val_overcrowd integer NOT NULL,
    num_wc_recs integer NOT NULL,
    num_sp1_recs integer NOT NULL,
    num_sp2_recs integer NOT NULL,
    dwell_tot_mins double precision NOT NULL,
    cars integer NOT NULL
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tridelta
    OWNER to postgres;

COMMENT ON TABLE public.tridelta
    IS 'AC Transit APC data.';

COMMENT ON COLUMN public.tridelta.stop_id
    IS 'Unique stop ID';

COMMENT ON COLUMN public.tridelta.stop_name
    IS 'Name of the stop';

COMMENT ON COLUMN public.tridelta.route
    IS 'Route ID';

COMMENT ON COLUMN public.tridelta.trip
    IS 'Scheduled trip start time (text: 4 characters)';

COMMENT ON COLUMN public.tridelta.stop_seq_id
    IS 'Stop sequence number on route';

COMMENT ON COLUMN public.tridelta.bus
    IS 'Vehicle ID';

COMMENT ON COLUMN public.tridelta.act_stop_time
    IS 'Actual arrival time at the stop';

COMMENT ON COLUMN public.tridelta.direction
    IS 'Direction code';

COMMENT ON COLUMN public.tridelta.latitude
    IS 'Latitude of the stop (no correction)';

COMMENT ON COLUMN public.tridelta.longitude
    IS 'Longitude of the stop (no correction)';

COMMENT ON COLUMN public.tridelta.psgr_on
    IS 'Number of passengers boarding at stop';

COMMENT ON COLUMN public.tridelta.psgr_off
    IS 'Number of passengers deboarding at stop';

COMMENT ON COLUMN public.tridelta.psgr_load
    IS 'The total number of passengers on the bus at stop departure';

COMMENT ON COLUMN public.tridelta.val_full
    IS 'Values of Full capacity for bus';

COMMENT ON COLUMN public.tridelta.val_overcrowd
    IS 'Overcrowding values for bus';

COMMENT ON COLUMN public.tridelta.num_wc_recs
    IS 'Number of wheelchair records at this stop';

COMMENT ON COLUMN public.tridelta.num_sp1_recs
    IS 'Number of 1st bike rack records at this stop';

COMMENT ON COLUMN public.tridelta.num_sp2_recs
    IS 'Number of 2nd bike rack records at this stop';
