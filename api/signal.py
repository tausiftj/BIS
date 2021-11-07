from celery.decorators import task



@task
def save_booking(self, request, *args, **kwargs):
    data = request.data
    data['created_by'] = request.user.id
    serializer = self.get_serializer(data=data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)


@task
def cancelled_booking(self, request):
    instance = self.get_object()
    instance.update(status='cancelled')

@task
def update_booking(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)

    if getattr(instance, '_prefetched_objects_cache', None):
        # If 'prefetch_related' has been applied to a queryset, we need to
        # forcibly invalidate the prefetch cache on the instance.
        instance._prefetched_objects_cache = {}