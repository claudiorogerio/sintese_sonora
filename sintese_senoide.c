// sudo apt-get install libopenal-dev
// gcc -o sintese_senoide   sintese_senoide.c  -lopenal -lm

#include <stdio.h>
#include <stdlib.h>    
#include <math.h>

#ifdef __APPLE__
#include <OpenAL/al.h>
#include <OpenAL/alc.h>
#elif __linux
#include <AL/al.h>
#include <AL/alc.h>
#include <unistd.h>
#endif

ALCdevice  * openal_output_device;
ALCcontext * openal_output_context;
ALuint internal_buffer;     // buffer sonoro
ALuint streaming_source[1]; // stream gerado

// Funcao padrao para erros
int al_check_error(const char * given_label) {
    ALenum al_error;
    al_error = alGetError();
    if(AL_NO_ERROR != al_error) {
        printf("ERROR - %s  (%s)\n", alGetString(al_error), given_label);
        return al_error;
    }
    return 0;
}

// inicializacao
void MM_init_all() {

    const char * defname = alcGetString(NULL, ALC_DEFAULT_DEVICE_SPECIFIER);

    openal_output_device  = alcOpenDevice( defname );
    openal_output_context = alcCreateContext( openal_output_device, NULL );
    alcMakeContextCurrent( openal_output_context );
    // setup buffer and source
    alGenBuffers(1, & internal_buffer );
    al_check_error("failed call to alGenBuffers");
}

// clean
void MM_exit_all() {

    ALenum errorCode = 0;
    // Stop the sources
    alSourceStopv(1, & streaming_source[0]);        //      streaming_source
    int ii;
    for (ii = 0; ii < 1; ++ii) {
        alSourcei(streaming_source[ii], AL_BUFFER, 0);  }
    // Clean-up
    alDeleteSources(1, &streaming_source[0]);
    alDeleteBuffers(16, &streaming_source[0]);
    errorCode = alGetError();
    alcMakeContextCurrent(NULL);
    errorCode = alGetError();
    alcDestroyContext(openal_output_context);
    alcCloseDevice(openal_output_device);
}

// gerador de senoides
void MM_render_one_buffer( float freq ) {

    float incr_freq = 0.06f;
    int seconds = 4;
    // unsigned sample_rate = 22050;    // testes com diferentes rates
    unsigned sample_rate = 44100;
    double my_pi = 3.14159;
    size_t buf_size = seconds * sample_rate;

    // allocate PCM audio buffer vetor de samples        
    short * samples = malloc(sizeof(short) * buf_size);

    printf("\nFreq senoide: %f\n", freq);
    int i=0;
    for(; i<buf_size; ++i) {
        samples[i] = 32760 * sin( (2.f * my_pi * freq)/sample_rate * i );
        freq += incr_freq;  
        if (100.0 > freq || freq > 2000.0) 
            incr_freq *= -1.0f;  // toggle direction of freq increment
        if (3000.0 > freq || freq > 5000.0) 
            incr_freq *= 1.0f;  // toggle direction of freq increment           
    }

    /* atualizando o internal_buffer com a senoide criada para o OpenAL */
    alBufferData( internal_buffer, AL_FORMAT_MONO16, samples, buf_size, sample_rate);
    al_check_error("populating alBufferData");

    free(samples);
    
    alGenSources(1, & streaming_source[0]); // cria um stream
    alSourcei(streaming_source[0], AL_BUFFER, internal_buffer); // adiciona buffer ao stream
    alSourcePlay(streaming_source[0]); // play stream

    // ---------------------

    ALenum current_playing_state;
    alGetSourcei(streaming_source[0], AL_SOURCE_STATE, & current_playing_state);
    al_check_error("alGetSourcei AL_SOURCE_STATE");

    while (AL_PLAYING == current_playing_state) {

        printf("playing ... so sleep\n");
        sleep(1);   // should use a thread sleep NOT sleep() for a more responsive finish
        alGetSourcei(streaming_source[0], AL_SOURCE_STATE, & current_playing_state);
        al_check_error("alGetSourcei AL_SOURCE_STATE");
    }

    printf("end of playing\n");

    MM_exit_all();
}  

int main() {

    MM_init_all();
    MM_render_one_buffer( 400.0 );
}
