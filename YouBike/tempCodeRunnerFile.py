    header = fp.readline()
        reader = csv.reader( fp, delimiter="," )
        all_data = [ [ row[ i ] for i in range( 6 ) ] for row in reader ]
        return (
            all_data,
            [ [ float( row[ 2 ] ), float( row[ 3 ] ) ] for row in all_data ],
            [ float( row[ 4 ] ) for row in all_data ],
            float( all_data[ 0 ][ 5 ] ),
        )