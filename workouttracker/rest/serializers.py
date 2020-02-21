from rest_framework import serializers

from workouttracker.models import Routine, RoutineExercise, Exercise, Workout, WorkoutExercise, Run

class RoutineExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineExercise
        fields = ('id', 'title', 'description', 'reps', 'sets', 'setsCompleted', 'routine')

    # transfer id for update actions
    id = serializers.IntegerField(required=False)

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = ('id', 'title', 'description', 'reps', 'sets', 'setsCompleted', 'workout')

    # transfer id for update actions
    id = serializers.IntegerField(required=False)

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ('id', 'name', 'description')
        read_only_fields = ('last_modified',)

    routineexercises = RoutineExerciseSerializer(many=True)

    def validate(self, data):
        return data

    def create(self, validated_data):
        routineexercise_data = validated_data.pop('routineexercises')
        routine = Routine.objects.create(**validated_data)

        for routineexercise in routineexercise_data:
            RoutineExercise.objects.create(routine=routine, **routineexercise)
        return routine

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description',
                                                       instance.description)
        instance.save()
        for routineexercise in validated_data.get('routineexercises'):
            routineexercise_object = RoutineExercise.objects.get(id=routineexercise.get('id'))

            routineexercise_object.title = routineexercise.get('title', routineexercise_object.title)
            routineexercise_object.description = routineexercise.get('description', routineexercise_object.description)
            routineexercise_object.account = routineexercise.get('reps', routineexercise_object.reps)
            routineexercise_object.account = routineexercise.get('sets', routineexercise_object.sets)
            routineexercise_object.save()
        return instance


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ('id', 'date', 'description')
        read_only_fields = ('last_modified',)

    workoutexercises = WorkoutExerciseSerializer(many=True)

    def validate(self, data):
        return data

    def create(self, validated_data):
        workoutexercise_data = validated_data.pop('workoutexercises')
        workout = Workout.objects.create(**validated_data)

        for workoutexercise in workoutexercise_data:
            WorkoutExercise.objects.create(workout=workout, **workoutexercise)
        return workout

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description',
                                                       instance.description)
        instance.save()

        for workoutexercise in validated_data.get('workoutexercises'):
            workoutexercise_object = WorkoutExercise.objects.get(id=workoutexercise.get('id'))

            workoutexercise_object.title = workoutexercise.get('title', workoutexercise_object.title)
            workoutexercise_object.description = workoutexercise.get('description', workoutexercise_object.description)
            workoutexercise_object.account = workoutexercise.get('reps', workoutexercise_object.reps)
            workoutexercise_object.account = workoutexercise.get('sets', workoutexercise_object.sets)
            workoutexercise_object.save()
        return instance

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'title', 'date', 'exercise_type', 'last_modified')
        read_only_fields = ('last_modified',)


    def validate(self, data):
        return data

    def create(self, validated_data):
        exercise = Exercise.objects.create(**validated_data)
        return exercise

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ('id', 'date', 'description', 'distance', 'time')

    date = serializers.DateField()
    description = serializers.CharField()
    distance = serializers.DecimalField(max_digits=6, decimal_places=2)
    time = serializers.DecimalField(max_digits=6, decimal_places=2)

    def validate(self, data):
        return data

    def create(self, validated_data):
        run = Run.objects.create(**validated_data)
        return run

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ('id', 'name', 'description', 'last_modified')
        read_only_fields = ('last_modified',)