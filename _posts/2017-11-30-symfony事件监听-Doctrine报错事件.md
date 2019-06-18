# symfony(3.3)框架使用事件监听(eventlistener)创建

判断出event的exception是否是 Doctrine的exception 如果是返回event response

```php

<?php
namespace AppBundle\EventListener;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpKernel\Event\GetResponseForExceptionEvent;
use Doctrine\DBAL\Exception\ConnectionException;

class ExceptionListener
{
    public function onKernelException(GetResponseForExceptionEvent $event)
    {
        // You get the exception object from the received event
        // 你可以从接收到的事件中，取得异常对象
        $exception = $event->getException();
        //监听数据库连接失败的信息
        if ($exception instanceof ConnectionException) {
            $message = sprintf(
                'db error %s',
                $exception->getMessage()
            );
            // Customize your response object to display the exception details
            // 自定义响应对象，来显示异常的细节
            $response = new JsonResponse(array('code'=>510,'msg'=>$message,'data'=>""));
            $event->setResponse($response);
        }
    }
}

```

service.yml

```YAML
    app.exception_listener:
        class: AppBundle\EventListener\ExceptionListener
        tags:
            - { name: kernel.event_listener, event: kernel.exception }
```