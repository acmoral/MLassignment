import jams
import numpy as np

diccionario_tonicas = { 
    'C': 0,
    'C#': 1,
    'D': 2,
    'D#': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'G': 7,
    'G#': 8,
    'A': 9,
    'A#': 10,
    'B': 11
}
diccionario_acordes = {
    'maj': [0, 4, 7],
    'min': [0, 3, 7],
    '7': [0, 4, 7, 10],
    'maj7': [0, 4, 7, 11],
    'min7': [0, 3, 7, 10],
    'dim': [0, 3, 6],
    'dim7': [0, 3, 6, 9],
    'aug': [0, 4, 8],
    'aug7': [0, 4, 8, 10],
    'sus2': [0, 2, 7],
    'sus4': [0, 5, 7],
    '7sus4': [0, 5, 7, 10],
    '6': [0, 4, 7, 9],
    'm6': [0, 3, 7, 9],
    '9': [0, 4, 7, 10, 14],
    'maj9': [0, 4, 7, 11, 14],
    'min9': [0, 3, 7, 10, 14],
    '11': [0, 4, 7, 10, 14, 17],
    'maj11': [0, 4, 7, 11, 14, 17],
    'min11': [0, 3, 7, 10, 14, 17],
    '13': [0, 4, 7, 10, 14, 17, 21],
    'maj13': [0, 4, 7, 11, 14, 17, 21],
    'min13': [0, 3, 7, 10, 14, 17, 21],
    '7#9': [0, 4, 7, 10, 15],
    '7b9': [0, 4, 7, 10, 13],
    '7#5': [0, 4, 8, 10],
    '7b5': [0, 4, 6, 10],
    'hdim7': [0, 3, 6, 10],
    }
scale_modes = {
#major
    'ionian': [0, 2, 4, 5, 7, 9, 11],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'aeolian': [0, 2, 3, 5, 7, 8, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
#minor_melodic
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'phrygian_natural_6': [0, 1, 3, 5, 7, 8, 10],
    'lydian_augmented': [0, 1, 4, 6, 8, 9, 11],
    'lydian_dominant': [0, 2, 4, 6, 7, 9, 10],
    'mixolydian_b6': [0, 2, 4, 5, 7, 8, 10],
    'half_diminished': [0, 2, 3, 5, 6, 8, 10],
    'altered': [0, 1, 3, 4, 6, 8, 20]
}
def longest_contiguous_common_subsequence(A, B):
    m = len(A)
    n = len(B)
    
    # Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Variables to keep track of the maximum length and ending position
    max_len = 0
    end_pos = 0
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i - 1  # or j - 1, both are same in case of contiguous subsequence
            else:
                dp[i][j] = 0
    
    # If max_len is 0, no contiguous common subsequence exists
    if max_len == 0:
        return None
    
    # Retrieve longest contiguous common subsequence
    result = A[end_pos - max_len + 1:end_pos + 1]
    return result
# Función para encontrar la duración permitida más cercana a una duración dada en segundos
def encontrar_duracion_permitida(duracion, duraciones_permitidas_seg):
    duracion_permitida_cercana = min(duraciones_permitidas_seg.values(), key=lambda x: abs(x - duracion))
    return duracion_permitida_cercana
# Función para representar una duración como un vector binario
def duracion_a_vec(duracion, duraciones_permitidas_seg):
    duracion_permitida_cercana = encontrar_duracion_permitida(duracion, duraciones_permitidas_seg)
    vector_binario = np.zeros(len(duraciones_permitidas_seg))
    for i, duracion_permitida in enumerate(duraciones_permitidas_seg.values()):
        if duracion_permitida == duracion_permitida_cercana:
            vector_binario[i] = 1
    return vector_binario

# Función para representar un desfase como un vector binario
def offset_a_vec(offset, offsets_permitidos_seg):
    # Buscar el desfase permitido más cercano
    offset_permitido_cercano = min(offsets_permitidos_seg, key=lambda x:abs(x-offset))
    vector_binario = np.zeros(len(offsets_permitidos_seg))
    for i, offset_permitido in enumerate(offsets_permitidos_seg):
        if offset_permitido == offset_permitido_cercano:
            vector_binario[i] = 1
    return vector_binario
def acorde_a_vec(acorde):
    acorde_vec = np.zeros(12)
    tonica = acorde.value.split(':')[0]
    tipo_acorde = acorde.value.split(':')[1]
    idx_tonica = diccionario_tonicas[tonica]
    idx_tipo_acorde = diccionario_acordes[tipo_acorde]
    for idx in idx_tipo_acorde:
        acorde_vec[(idx_tonica + idx) % 12] = 1    
    return acorde_vec
def posibles_escalas_de_acorde(acorde):
    tonica = acorde.value.split(':')[0]
    tipo_acorde = acorde.value.split(':')[1]
    idx_tonica = diccionario_tonicas[tonica]
    idx_tipo_acorde = diccionario_acordes[tipo_acorde]
    possible_scales = []
    possible_scale_vecs = []

    for key in scale_modes.keys():
        if set(idx_tipo_acorde) <= set(scale_modes[key]):
            possible_scales.append(key)

    for scale in possible_scales:
        scale_vec = np.zeros(12)
        scale_idx = scale_modes[scale]
        for idx in scale_idx:
            scale_vec[(idx_tonica + idx) % 12] = 1
        possible_scale_vecs.append(scale_vec)
    return possible_scale_vecs

# Función para dividir un silencio largo en duraciones permitidas
def dividir_silencio(delta_t,max_dur,duraciones_permitidas_seg): 
    duraciones_divididas = []
    while delta_t > max_dur:
        duracion_permitida = encontrar_duracion_permitida(delta_t, duraciones_permitidas_seg)
        duraciones_divididas.append(duracion_permitida)
        delta_t -= duracion_permitida
    if delta_t <= max_dur:
        duracion_permitida = encontrar_duracion_permitida(delta_t, duraciones_permitidas_seg)
        duraciones_divididas.append(duracion_permitida)
        
    return duraciones_divididas


def jams_a_vec(ruta_archivo_jams):
    # Cargar el archivo JAMS
    jam = jams.load(ruta_archivo_jams)

    # Buscar anotaciones de notas MIDI
    notes = jam.search(namespace='note_midi')
    chords = jam.search(namespace='chord')[0].data

    # Obtener el valor de los BPM (tempo)
    bpm = jam.search(namespace='tempo')[0].data[0].value
    bps = bpm / 60
    # Duración de negra en segundos
    quater_duration = 1 / bps
    # Duraciones permitidas en segundos (de menor a mayor)
    duraciones_permitidas_seg = {
        'fusa': quater_duration / 8,
        'tresillo_semicorchea': quater_duration / 6,
        'fusa_puntillo': 1.5 * quater_duration / 8,
        'semicorchea': quater_duration / 4,
        'tresillo_corchea': quater_duration / 3,
        'semicorchea_puntillo': 1.5 * quater_duration / 4,
        'corchea': quater_duration / 2,
        'tresillo': (2 / 3) * quater_duration,
        'corchea_puntillo': 1.5 * quater_duration / 2,
        'negra': quater_duration,
        'negra_puntillo': quater_duration * 1.5,
        'blanca': 2 * quater_duration,
        'blanca_puntillo': 2 * quater_duration * 1.5,
        'redonda': 4 * quater_duration,
    }
    # Duración mínima permitida
    duracion_minima = duraciones_permitidas_seg['fusa']
    tresillo_minimo = quater_duration / 6
    # Definir los desfases permitidos en segundos
    #max_offset = 4 * quater_duration - duracion_minima
    offsets_permitidos_seg = [i * duracion_minima for i in range(31)]
    # Añadir múltiplos de tresillos al diccionario de desfases permitidos
    num_tresillos = 23
    for i in range(1,num_tresillos):
        offset_tresillo = i * tresillo_minimo
        offsets_permitidos_seg.append(offset_tresillo)
    # Ordenar los desfases permitidos
    offsets_permitidos_seg.sort()
    # Extraer todas las notas
    all_notes = [note for sublist in [list(note.data) for note in notes] for note in sublist]
    all_chords = [chord for chord in chords]
    # Ordenar las notas por tiempo
    all_notes.sort(key=lambda x: x.time)
    all_chords.sort(key=lambda x: x.time)
    #inicializar listas
    pitch_vec0 = np.zeros(128)
    pitch_vec0[round(all_notes[0].value)] = 1
    pitch_vecs = [pitch_vec0]
    dur_vecs = [duracion_a_vec(all_notes[0].duration,duraciones_permitidas_seg)]
    offset_vecs = [offset_a_vec(all_notes[0].time,offsets_permitidos_seg)]

    curr_chord_idx = 0

    acorde_actual = all_chords[curr_chord_idx]
    chord_vecs = [acorde_a_vec(acorde_actual)]
    possible_scales = [posibles_escalas_de_acorde(acorde_actual)]
    # Iterar sobre las notas ordenadas
    for i in range(1,len(all_notes)):
        note = all_notes[i]
        last_note = all_notes[i-1]
        pitch_vec = np.zeros(128)
        duration = note.duration
        pitch_midi = note.value
        offset = note.time-last_note.time
        # Redondear pitch
        midi_note = round(pitch_midi)
        pitch_vec[midi_note] = 1
        # Añadir vector de pitch a la lista
        pitch_vecs.append(pitch_vec)
        dur_vecs.append(duracion_a_vec(duration,duraciones_permitidas_seg))
        offset_vecs.append(offset_a_vec(offset,offsets_permitidos_seg))
        #encargarse de los acordes
        acorde_actual = all_chords[curr_chord_idx]
        chord_time = acorde_actual.time
        chord_duration = acorde_actual.duration
        #verificamos si el comienzo de la nota está entre comienzo de acorde y final de acorde
        #si no, cambiamos a siguiente acorde y agregamos a lista
        if note.time > chord_time + chord_duration:
            curr_chord_idx += 1
            acorde_vec = acorde_a_vec(all_chords[curr_chord_idx])
            chord_vecs.append(acorde_vec)
            possible_scales.append(posibles_escalas_de_acorde(all_chords[curr_chord_idx]))
        else:
            acorde_vec = acorde_a_vec(all_chords[curr_chord_idx])
            chord_vecs.append(acorde_vec)
            possible_scales.append(posibles_escalas_de_acorde(all_chords[curr_chord_idx]))
    return pitch_vecs, dur_vecs, offset_vecs, chord_vecs,possible_scales
